import pandas as pd
 
def compare_data(source_file, target_file, column_name):
    # Read source and target CSV files
    source_data = pd.read_csv(source_file)
    target_data = pd.read_csv(target_file)
 
    # Compare 'id' column between source and target dataframes
    rejected_records = source_data[~source_data[column_name].isin(target_data[column_name])]
 
    return rejected_records