import pandas as pd


def change_data_types(df, mismatched_columns):
    for column, expected_type in mismatched_columns:
        df[column] = df[column].astype(expected_type)
        print(f"✅ Changed data type of '{column}' to {expected_type}")

    return df
