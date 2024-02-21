import pandas as pd

def Check_Duplicate(source_df, target_df, sid_column, tid_column):
    # Check for duplicate columns in source and target dataframes
    duplicate_columns_source = source_df.columns.duplicated().any()
    duplicate_columns_target = target_df.columns.duplicated().any()

    # Check for duplicate rows based on the specified ID column
    duplicate_rows_source = source_df.duplicated(subset=[sid_column]).any()
    duplicate_rows_target = target_df.duplicated(subset=[tid_column]).any()

    if duplicate_columns_source or duplicate_columns_target:
        print("Validation failed: Duplicate columns found in either source or target CSV files.")
        return {"Duplicate columns in source": duplicate_columns_source, "Duplicate columns in target": duplicate_columns_target}

    if duplicate_rows_source or duplicate_rows_target:
        print("Validation failed: Duplicate rows found based on the specified ID column.")
        return {"Duplicate rows in source": duplicate_rows_source, "Duplicate rows in target": duplicate_rows_target}

    return "Validation successful: No duplicate columns or rows found."

