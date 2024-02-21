import pandas as pd

def Data_Validation(source_df, target_df, column):
    # Check if the data in the specified column is the same in both dataframes
    different_records = source_df[source_df[column] != target_df[column]]

    if different_records.empty:
        return "Data validation successful: Data in column '{}' is the same in both source and target dataframes.".format(column)
    else:
        return different_records

