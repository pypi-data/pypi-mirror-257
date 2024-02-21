import pandas as pd

def Out_of_range(target_df, column_name, max_length, expected_dtype):
    # Check if column exists
    if column_name not in target_df.columns:
        print(f"Column '{column_name}' not found in the DataFrame.")
        return
 
    # Data correctness validation
    print(f"Performing data correctness validation for column '{column_name}':")
    validation_passed = True  # Flag to track validation status
   
    # Out of range data check
    if max_length is not None:
        exceeding_length = target_df[target_df[column_name].astype(str).str.len() > max_length]
        if not exceeding_length.empty:
            print("Validation failed: Rows with data exceeding maximum length.")
            print(exceeding_length)
            validation_passed = False
   
    # Check data type
    if expected_dtype is not None:
        wrong_dtype = target_df[~target_df[column_name].apply(lambda x: isinstance(x, expected_dtype))]
        if not wrong_dtype.empty:
            print("Validation failed: Rows with incorrect data type.")
            print(wrong_dtype)
            validation_passed = False
 
    if validation_passed:
        print("Validation passed: All data comply with the given input.")
    else:
        print("Validation failed: Data does not comply with the given input.")
 