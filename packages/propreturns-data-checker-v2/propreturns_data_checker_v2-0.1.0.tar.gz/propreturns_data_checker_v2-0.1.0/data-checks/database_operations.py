import pandas as pd
from sqlalchemy import create_engine
from psycopg2.extensions import register_adapter, AsIs
import configparser
import numpy as np

config = configparser.ConfigParser()
config.read("config.ini")


def append_to_sql_table_segregate(df, db_name, table_name, action_to_perform="append"):
    register_adapter(np.int64, AsIs(np.int64))

    config = configparser.ConfigParser()
    config.read("config.ini")

    user = config.get("database", "user")
    password = config.get("database", "password")
    host = config.get("database", "host")
    port = config.get("database", "port")

    conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    db = create_engine(conn_string)

    try:
        df.to_sql(table_name, con=db, if_exists=action_to_perform, index=False)
        print(f"Data Uploaded to {table_name}")
    except Exception as e:
        # Handle the case where the table doesn't exist
        if "relation" in str(e) and "does not exist" in str(e):
            print(
                f"Table '{table_name}' not found. Creating a new table and uploading data."
            )
            df.to_sql(table_name, con=db, if_exists="replace", index=False)
            print(f"Data Uploaded to {table_name}")
        else:
            print(f"Error: {e}")
