
import pandas as pd

def Data_Truncation_specified_columns(source_df, target_df, columns_to_check):

    truncation_info = []

    for column in columns_to_check:
        source_lengths = source_df[column].astype(str).str.len()
        target_lengths = target_df[column].astype(str).str.len()
        truncated_records = target_df[target_lengths < source_lengths]
        
        truncation_info.append({
            "column": column,
            "truncated_records": truncated_records
        })

    return truncation_info

