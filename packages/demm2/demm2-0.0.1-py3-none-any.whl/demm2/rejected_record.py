import pandas as pd
 
def compare_data(source_df, target_df, column_name):

    rejected_records = source_df[~source_df[column_name].isin(target_df[column_name])]
 
    return rejected_records