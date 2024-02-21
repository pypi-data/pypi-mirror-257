import pandas as pd


def check_missing_values(df, data_type):
    """
    Check for missing values in required columns for sale and lease data.

    Parameters:
    - df: pandas DataFrame
    - data_type: string specifying the type of data ('sale' or 'lease')

    Returns:
    - DataFrame of missing rows
    """
    if data_type.lower() == "sale":
        required_columns = [
            "builtup_area",
            "carpet_area",
            "submission_date",
            "transaction_price",
            "price_per_sq_ft_acc_to_transaction_price",
        ]
    elif data_type.lower() == "lease":
        required_columns = [
            "builtup_area",
            "carpet_area",
            "rent_per_month",
            "rent_per_sq_ft",
        ]
    else:
        print("Invalid data type specified.")
        return pd.DataFrame()  # Return an empty DataFrame if an invalid data type

    missing_rows = df[df[required_columns].isnull().any(axis=1)]

    if not missing_rows.empty:
        print(
            "⚠️ Hold your horses! We found some missing values. Let's check it out! 🕵️‍♂️"
        )

        # Check the number of missing transaction IDs
        unique_transaction_ids = missing_rows["transaction_id"].unique()
        if len(unique_transaction_ids) > 100:
            print(
                "⚠️ Whoa! There are more than 100 missing transactions! Saving them to a CSV file. 📁"
            )
            missing_transactions_df = pd.DataFrame(
                {"transaction_id": unique_transaction_ids}
            )
            missing_transactions_df.to_csv(
                f"missing_transactions_{data_type}.csv", index=False
            )
            print("✅ Saved missing transaction IDs to 'missing_transactions.csv'")
        else:
            print(f"⚠️ Missing transaction IDs ({len(unique_transaction_ids)}):")
            for transaction_id in unique_transaction_ids:
                print(f"   Transaction ID: {transaction_id}")
            print(
                "🚨 Hold on! There are still issues. Pause on pushing to production! ⛔"
            )
    else:
        print("✅ No missing values in required columns. Proceeding with other checks.")

    return missing_rows
