import pandas as pd

def filter_first_csv(input_file):
    df = pd.read_csv(input_file, delimiter=';')
    print("First CSV columns:", df.columns)
    df_filtered = df[df['CHECK_TYPE'].str.contains('CIS AWS Foundations Benchmark', na=False)]
    if df_filtered.empty:
        print("No rows found with 'CIS AWS Foundations Benchmark'. Trying with 'CIS' instead.")
        df_filtered = df[df['CHECK_TYPE'].str.contains('CIS', na=False)]
    required_columns = ['CHECK_ID','SERVICE_NAME','CHECK_TITLE','SEVERITY', 'STATUS']
    df_filtered = df_filtered[required_columns]
    return df_filtered

def filter_second_csv(second_input_file):
    df = pd.read_csv(second_input_file) 
    print("Second CSV columns:", df.columns)
    required_columns = ['ID', 'Category', 'Name', 'Severity','TestResult']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing columns in second CSV: {missing_columns}")
        return pd.DataFrame()
    df_filtered = df[required_columns]   
    print("Filtered df2 columns:", df_filtered.columns)
    return df_filtered

def merge_csv(df1, df2):
    df1['SEVERITY'] = df1['SEVERITY'].str.lower()
    df2['Severity'] = df2['Severity'].str.lower()
    status_mapping = {
        r'^\s*PASS\s*$': 'Passed', r'^\s*pass\s*$': 'Passed', r'^\s*passed\s*$': 'Passed',
        r'^\s*FAIL\s*$': 'Failed', r'^\s*fail\s*$': 'Failed', r'^\s*failed\s*$': 'Failed',
        r'^\s*None\s*$': 'Failed', r'^\s*none\s*$': 'Failed'
    }
    df1['STATUS'] = df1['STATUS'].str.strip().replace(status_mapping, regex=True)
    df2['TestResult'] = df2['TestResult'].str.strip().replace(status_mapping, regex=True)
    check_id = pd.concat([df1['CHECK_ID'], df2['ID']], ignore_index=True)
    category_name = pd.concat([df1['SERVICE_NAME'], df2['Category']], ignore_index=True)
    check_name = pd.concat([df1['CHECK_TITLE'], df2['Name']], ignore_index=True)
    severity = pd.concat([df1['SEVERITY'], df2['Severity']], ignore_index=True)
    status = pd.concat([df1['STATUS'], df2['TestResult']], ignore_index=True)
    final_df = pd.DataFrame({
        'Check_ID': check_id,
        'Category_Name': category_name,
        'Check_Name': check_name,
        'Severity': severity,
        'Status': status
    })
    final_df.dropna(how='all', inplace=True)
    return final_df

def save_to_csv(final_df, output_file):
    final_df.to_csv(output_file, index=False)
    print(f"Merged CSV saved as {output_file}")


# combines csv files 
def main():
    print("Enter the type of files to process:")
    print("1: Prowler CSV files")
    print("2: Harden Windows CSV files")
    file_type = input("Enter 1 or 2: ")
    if file_type == '1':
        file_list = []
        while True:
            file_path = input("Enter the path to a Prowler CSV file (or press Enter to finish): ")
            if file_path == '':
                break
            file_list.append(file_path)
        if not file_list:
            print("No files provided. Exiting.")
            return
        df_list = []
        for file in file_list:
            df = filter_first_csv(file)
            if not df.empty:
                df_list.append(df)
        if not df_list:
            print("No valid dataframes from the provided files.")
            return
        df1 = pd.concat(df_list, ignore_index=True)
        file_list_2 = []
        print("Now, please provide Harden Windows CSV files.")
        while True:
            file_path = input("Enter the path to a Harden Windows CSV file (or press Enter to finish): ")
            if file_path == '':
                break
            file_list_2.append(file_path)
        if not file_list_2:
            print("No Harden Windows files provided.")
            df2 = pd.DataFrame()
        else:
            df_list_2 = []
            for file in file_list_2:
                df = filter_second_csv(file)
                if not df.empty:
                    df_list_2.append(df)
            if not df_list_2:
                print("No valid Harden Windows dataframes from the provided files.")
                df2 = pd.DataFrame()
            else:
                df2 = pd.concat(df_list_2, ignore_index=True)
        final_df = merge_csv(df1, df2)
        if not final_df.empty:
            output_csv = 'filtered_output.csv'
            save_to_csv(final_df, output_csv)
        else:
            print("Merged DataFrame is empty. No data to save.")
    elif file_type == '2':
        file_list = []
        while True:
            file_path = input("Enter the path to a Harden Windows CSV file (or press Enter to finish): ")
            if file_path == '':
                break
            file_list.append(file_path)
        if not file_list:
            print("No files provided. Exiting.")
            return
        df_list = []
        for file in file_list:
            df = filter_second_csv(file)
            if not df.empty:
                df_list.append(df)
        if not df_list:
            print("No valid dataframes from the provided files.")
            return
        df2 = pd.concat(df_list, ignore_index=True)
        file_list_2 = []
        print("Now, please provide Prowler CSV files.")
        while True:
            file_path = input("Enter the path to a Prowler CSV file (or press Enter to finish): ")
            if file_path == '':
                break
            file_list_2.append(file_path)
        if not file_list_2:
            print("No Prowler files provided.")
            df1 = pd.DataFrame()
        else:
            df_list_2 = []
            for file in file_list_2:
                df = filter_first_csv(file)
                if not df.empty:
                    df_list_2.append(df)
            if not df_list_2:
                print("No valid Prowler dataframes from the provided files.")
                df1 = pd.DataFrame()
            else:
                df1 = pd.concat(df_list_2, ignore_index=True)
        final_df = merge_csv(df1, df2)
        if not final_df.empty:
            output_csv = 'filtered_output.csv'
            save_to_csv(final_df, output_csv)
        else:
            print("Merged DataFrame is empty. No data to save.")
    else:
        print("Invalid option selected.")

if __name__ == "__main__":
    main()
