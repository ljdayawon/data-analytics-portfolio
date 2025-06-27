# This script prepares transaction data for mlxtend’s Apriori algorithm by 
# combining date and time into hourly transactions, assigning unique IDs, and 
# generating a True/False matrix of selected product categories.

import pandas as pd

#Load the Excel file
file_path = r"C:\Users\ADMIN\Desktop\IPT Final Project\ConvertToBinary.xlsx"
sheet_name = "MINED for Apriori"
df = pd.read_excel(file_path, sheet_name=sheet_name)

#Combine date and time, round to nearest hour
df['transaction_datetime'] = pd.to_datetime(df['transaction_date'].astype(str) + ' ' + df['transaction_time'].astype(str))
df['transaction_hour'] = df['transaction_datetime'].dt.floor('H')

#Map each unique hour to a numeric transaction ID
sorted_hours = sorted(df['transaction_hour'].unique())
transaction_id_map = {hour: idx + 1 for idx, hour in enumerate(sorted_hours)}
df['transaction_id'] = df['transaction_hour'].map(transaction_id_map)

#Define item categories to track
desired_categories = [
    'Bakery',
    'Branded',
    'Coffee',
    'Coffee Beans',
    'Drinking Chocolate',
    'Flavours',
    'Loose Tea',
    'Packaged Chocolate',
    'Tea'
]

#Create binary matrix using crosstab
binary = pd.crosstab(df['transaction_id'], df['product_category'])

#Convert counts to boolean True/False
binary = binary.applymap(lambda x: x > 0)

#Ensure all desired categories are present
for cat in desired_categories:
    if cat not in binary.columns:
        binary[cat] = False

#Reorder columns and insert transaction_id
binary = binary[desired_categories]
binary.insert(0, 'transaction_id', binary.index)

#Save binary matrix to Excel
output_path = r"C:\Users\ADMIN\Desktop\IPT Final Project\ReadyForApriori.xlsx"
binary.to_excel(output_path, index=False)

print(f"TRUE / FALSE matrix saved to: {output_path}")
