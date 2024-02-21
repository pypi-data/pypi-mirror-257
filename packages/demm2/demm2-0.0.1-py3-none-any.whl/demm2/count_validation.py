import pandas as pd
# row count for same column name must same 
def Count_Validation(df1, df2):
    
    columns_df1 = set(df1.columns)
    columns_df2 = set(df2.columns)

    if columns_df1 != columns_df2:
        return "Column names are different between the two DataFrames."
    
    for column in columns_df1:
        count_df1 = df1[column].count()
        count_df2 = df2[column].count()
        
        if count_df1 != count_df2:
            return f"Counts do not match for column '{column}'! DataFrame 1 has {count_df1} rows, DataFrame 2 has {count_df2} rows."

    return "Counts match for all columns!"
