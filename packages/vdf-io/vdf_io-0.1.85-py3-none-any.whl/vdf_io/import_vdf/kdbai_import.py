from typing import Dict, List
from dotenv import load_dotenv
from tqdm import tqdm
import pyarrow.parquet as pq

import kdbai_client as kdbai

from vdf_io.names import DBNames
from vdf_io.import_vdf.vdf_import_cls import ImportVDB
from vdf_io.meta_types import NamespaceMeta
from vdf_io.util import (
    set_arg_from_input,
    set_arg_from_password,
    standardize_metric_reverse,
)

load_dotenv()

MAX_BATCH_SIZE = 10000


class ImportKDBAI(ImportVDB):
    DB_NAME_SLUG = DBNames.KDBAI

    @classmethod
    def import_vdb(cls, args):
        """
        Import data to KDB.AI
        """
        set_arg_from_input(
            args,
            "url",
            "Enter the endpoint for KDB.AI Cloud instance: ",
            str,
        )
        set_arg_from_password(
            args, "kdbai_api_key", "Enter your KDB.AI API key: ", "KDBAI_API_KEY"
        )
        set_arg_from_input(
            args,
            "index",
            "Enter the index type used (Flat, IVF, IVFPQ, HNSW): ",
            str,
        )
        kdbai_import = ImportKDBAI(args)
        kdbai_import.upsert_data()
        return kdbai_import

    @classmethod
    def make_parser(cls, subparsers):
        parser_kdbai = subparsers.add_parser(
            DBNames.KDBAI, help="Import data to KDB.AI"
        )
        parser_kdbai.add_argument(
            "-u", "--url", type=str, help="KDB.AI Cloud instance Endpoint url"
        )
        parser_kdbai.add_argument(
            "-i", "--index", type=str, help="Index used", default="hnsw"
        )

    def __init__(self, args):
        super().__init__(args)
        api_key = args.get("kdbai_api_key")
        endpoint = args.get("url")
        self.index = args.get("index")
        allowed_vector_types = ["flat", "ivf", "ivfpq", "hnsw"]
        if self.index.lower() not in allowed_vector_types:
            raise ValueError(
                f"Invalid vectorIndex type: {self.index}. "
                f"Allowed types are {', '.join(allowed_vector_types)}"
            )

        self.session = kdbai.Session(api_key=api_key, endpoint=endpoint)

    def upsert_data(self):
        total_imported_count = 0
        max_hit = False
        indexes_content: Dict[str, List[NamespaceMeta]] = self.vdf_meta["indexes"]
        index_names: List[str] = list(indexes_content.keys())
        if len(index_names) == 0:
            raise ValueError("No indexes found in VDF_META.json")

        # Load Parquet file
        # print(indexes_content[index_names[0]]):List[NamespaceMeta]
        for index_name, index_meta in tqdm(
            indexes_content.items(), desc="Importing indexes"
        ):
            for namespace_meta in tqdm(index_meta, desc="Importing namespaces"):
                data_path = namespace_meta["data_path"]
                final_data_path = self.get_final_data_path(data_path)
                index_name = index_name + (
                    f'_{namespace_meta["namespace"]}'
                    if namespace_meta["namespace"]
                    else ""
                )
                parquet_files = self.get_parquet_files(final_data_path)
                for parquet_file in tqdm(parquet_files, desc="Importing parquet files"):
                    parquet_file_path = self.get_file_path(
                        final_data_path, parquet_file
                    )
                    parquet_table = pq.read_table(parquet_file_path)
                    # rename columns by replacing "-" with "_"
                    parquet_table = parquet_table.rename_columns(
                        [col.replace("-", "_") for col in parquet_table.column_names]
                    )
                    parquet_schema = parquet_table.schema
                    parquet_columns = [
                        {"name": field.name, "type": str(field.type)}
                        for field in parquet_schema
                    ]

                    # Extract information from JSON
                    # namespace = indexes_content[index_names[0]][""][0]["namespace"]
                    (
                        vector_column_names,
                        vector_column_name,
                    ) = self.get_vector_column_name(index_name, namespace_meta)
                    vector_column_names = [
                        col.replace("-", "_") for col in vector_column_names
                    ]
                    vector_column_name = vector_column_name.replace("-", "_")
                    # Define the schema
                    schema = {
                        "columns": [
                            {
                                "name": vector_column_name,
                                "vectorIndex": {
                                    "dims": namespace_meta["dimensions"],
                                    "metric": standardize_metric_reverse(
                                        namespace_meta["metric"],
                                        self.DB_NAME_SLUG,
                                    ),
                                    "type": self.index.lower(),
                                },
                            }
                        ]
                    }

                    cols_to_be_dropped = []
                    # Add other columns from Parquet (excluding vector columns)
                    for col in parquet_columns:
                        if col["name"] not in vector_column_names:
                            schema["columns"].append(
                                {"name": col["name"], "pytype": col["type"]}
                            )
                        elif col["name"] != vector_column_name:
                            cols_to_be_dropped.append(col["name"])

                    for column in schema["columns"]:
                        if "pytype" in column and column["pytype"] == "string":
                            column["pytype"] = "str"

                    # First ensure the table does not already exist
                    try:
                        if index_name in self.session.list():
                            table = self.session.table(index_name)
                            tqdm.write(
                                f"Table '{index_name}' already exists. Upserting data into it."
                            )
                            # self.session.table(index_names).drop()
                        else:
                            table = self.session.create_table(index_name, schema)
                            tqdm.write("Table created")
                        # time.sleep(5)
                    except kdbai.KDBAIException as e:
                        tqdm.write(f"Error creating table: {e}")
                        raise RuntimeError(f"Error creating table: {e}")

                    # insert data
                    # Set the batch size
                    df = parquet_table.to_pandas().drop(columns=cols_to_be_dropped)
                    if total_imported_count + len(df) >= self.args["max_num_rows"]:
                        max_hit = True
                        # Take a subset of df
                        df = df.iloc[: self.args["max_num_rows"] - total_imported_count]
                    i = 0
                    batch_size = MAX_BATCH_SIZE
                    pbar = tqdm(total=df.shape[0], desc="Inserting data")
                    while i < df.shape[0]:
                        chunk = df[i : i + batch_size].reset_index(drop=True)
                        # Assuming 'table' has an 'insert' method
                        try:
                            table.insert(chunk)
                            pbar.update(chunk.shape[0])
                            i += batch_size
                        except kdbai.KDBAIException as e:
                            if "smaller batches" in str(e):
                                tqdm.write(
                                    f"Reducing batch size to {batch_size * 2 // 3}"
                                )
                                batch_size = batch_size * 2 // 3
                            else:
                                raise RuntimeError(f"Error inserting chunk: {e}")
                            continue
                    total_imported_count += len(df)
                    if max_hit:
                        break
                if max_hit:
                    break
            if max_hit:
                tqdm.write(
                    f"Max rows to be imported {self.args['max_num_rows']} hit. Exiting"
                )
                break

        # table.insert(df)
        print("Data imported successfully")
        self.args["imported_count"] = total_imported_count
