# data_checker/data_checker.py
import pandas as pd
from .data_types import check_data_types
from .missing_values import check_missing_values
from .duplicates import check_duplicates
from .database_operations import append_to_sql_table_segregate
from ..slack.slack_operations import send_slack_message
from ..utils.common_utils import change_data_types


def data_checker(df, data_type, db_name, table_name, action_to_perform="append"):
    try:
        mismatched_columns = check_data_types(df, data_type)

        if mismatched_columns:
            print("⚠️ Attention! Mismatched data types detected. Let's address that! 🛠️")
            df = change_data_types(df, mismatched_columns)
            print(
                "🎉 All good now! Data types are aligned. Proceeding with other checks."
            )
            mismatched_columns = check_data_types(df, data_type)
        else:
            print(
                f"✅ Data types for {data_type} data are accurate. Ready to proceed with changes."
            )

        missing_rows = check_missing_values(df, data_type)
        check_duplicates(df)

        if mismatched_columns or not missing_rows.empty:
            print(
                "🚨 Hold on! There are still issues. Pause on pushing to production! ⛔"
            )
            print("Issues:")
            if not missing_rows.empty:
                print(" - Missing values in required columns.")
                print(missing_rows["transaction_id"].to_string(index=False))
                send_slack_message(
                    f'⚠️ Missing values in required columns\n{", ".join(missing_rows["transaction_id"].astype(str))}',
                    db_name,
                    table_name,
                    action_to_perform,
                )

        else:
            print("✅ Everything's in order! Pushing data to PostgreSQL... 🚀")
            send_slack_message(
                "✅ Data pushed to PostgreSQL", db_name, table_name, action_to_perform
            )
            append_to_sql_table_segregate(df, db_name, table_name, action_to_perform)
    except Exception as e:
        print(f"Error in data_checker: {e}")
