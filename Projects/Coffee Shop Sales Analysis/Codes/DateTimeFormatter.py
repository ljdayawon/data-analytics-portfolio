# This script reads transaction data from Excel, verifies necessary columns, 
# combines date and time into a single datetime column, and saves the cleaned output 
# with transaction IDs to a new file, including error handling for file and data issues.

import pandas as pd

#Define the input and output file names
input_file = r"C:\Users\ADMIN\Desktop\IPT Final Project\Transactions.xlsx"
sheet_name = "Sheet1"
#The output file where the modified data will be saved.
output_file = r"C:\Users\ADMIN\Desktop\IPT Final Project\Transactions_formatted.xlsx"

#Read the data from the Excel file
try:
    #Read the specified sheet from the Excel file into a pandas DataFrame.
    df = pd.read_excel(input_file, sheet_name=sheet_name)
    print(f"Successfully read data from '{input_file}' - Sheet: '{sheet_name}'")
except FileNotFoundError:
    #Handle the case where the input file does not exist.
    print(f"ERROR: The file '{input_file}' was not found.")
    exit(1) #Exit the script if the file is not found.
except ValueError as e:
    #Handle cases where the sheet name might be incorrect or other reading errors occur.
    print(f"ERROR: Could not read sheet '{sheet_name}' from '{input_file}'. Details: {e}")
    exit(1) #Exit the script if reading fails.

#Display current columns for verification
print("Columns in DataFrame before combining:", df.columns.tolist())

#Check if 'transaction_id', 'transaction_date', and 'transaction_time' columns exist
required_columns = ['transaction_id', 'transaction_date', 'transaction_time']
for col in required_columns:
    if col not in df.columns:
        print(f"ERROR: Required column '{col}' not found in the Excel file.")
        print(f"Please ensure your Excel file has columns named {', '.join(required_columns)}.")
        exit(1) #Exit if essential columns are missing.

#Combine 'transaction_date' and 'transaction_time' columns

#Step 1: Convert 'transaction_date' to a proper datetime series.
#.dt.date extracts just the date part (e.g., '2023-01-01').
#pd.to_datetime then converts this date string back into a datetime object,
#setting the time component to 00:00:00.
df['transaction_date_only'] = pd.to_datetime(df['transaction_date'].dt.date)

#Step 2: Convert 'transaction_time' to a timedelta series.
#This step is crucial because time columns in Excel are often read as datetime objects
#where the date part is '1900-01-01'. We only need the time difference from midnight.
#.astype(str) converts the time column to string, then .str.split(' ').str[-1]
#extracts the actual time string (e.g., '07:06:11' from '1900-01-01 07:06:11').
#pd.to_timedelta then converts this time string into a timedelta object.
df['transaction_time_timedelta'] = pd.to_timedelta(df['transaction_time'].astype(str).str.split(' ').str[-1])

#Step 3: Add the timedelta to the date to get the combined datetime.
#This adds the time component from 'transaction_time_timedelta' to the 'transaction_date_only'.
df['datetime'] = df['transaction_date_only'] + df['transaction_time_timedelta']

#Prepare DataFrame for output with only 'transaction_id' and 'datetime'
#Select only the desired columns for the final output DataFrame.
df_output = df[['transaction_id', 'datetime']].copy()

#Save the modified DataFrame to a new Excel file
try:
    #Write the selected columns to a new Excel file.
    #index=False prevents pandas from writing the DataFrame index as a column.
    df_output.to_excel(output_file, index=False)
    print(f"Successfully saved the selected data to '{output_file}'")
except Exception as e:
    #Catch any errors during the saving process.
    print(f"ERROR: Could not save the output file to '{output_file}'. Details: {e}")

#Display the first few rows of the output DataFrame
print("\nFirst 5 rows of the output DataFrame with 'transaction_id' and 'datetime' columns:")
print(df_output.head())
