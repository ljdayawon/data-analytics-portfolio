import pandas as pd

# Load the original CSV
df = pd.read_csv(r"C:\Users\Lance - Work\Desktop\Projects\SQL\SuperStoreAnalysisSQL\CSV\Superstore_Dataset_cleanv2.csv")

# Convert date columns to datetime, forcing errors to NaT
df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')

# Format both columns as 'YYYY-MM-DD' string
df['Order_Date'] = df['Order_Date'].dt.strftime('%Y-%m-%d')
df['Ship_Date'] = df['Ship_Date'].dt.strftime('%Y-%m-%d')

# Export the cleaned CSV
df.to_csv(r"C:\Users\Lance - Work\Desktop\Projects\SQL\SuperStoreAnalysisSQL\CSVSuperstore_Dataset_cleanv2_FIXED.csv", index=False)

print("✅ Cleaned file saved as 'Superstore_Dataset_cleanv2_FIXED.csv'")
