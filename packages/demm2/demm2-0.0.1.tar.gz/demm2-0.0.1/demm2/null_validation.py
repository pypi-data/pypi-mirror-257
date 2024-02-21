import pandas as pd

def Null_Validation(source_df, target_df, column):

    nulls_source = source_df[column].isnull().any()
    nulls_target = target_df[column].isnull().any()

    if nulls_source or nulls_target:
        print(f"Null validation failed: Null values found in column '{column}' in either source or target dataframes.")
        return {"Nulls in source": nulls_source, "Nulls in target": nulls_target}
    else:
        return f"Null validation successful: No null values found in column '{column}' for both source and target dataframes."
