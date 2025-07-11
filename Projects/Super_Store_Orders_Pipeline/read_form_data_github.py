# --------------------------------------
# 📊 Superstore Orders Live Pipeline
# Description:
# - Reads live form responses from Google Sheets
# - Cleans and transforms customer name, order data, and product pricing
# - Merges with product catalog for cost/sales/profit analysis
# - Saves Tableau-ready output to a new worksheet
#
# Author: Lance Joseph Dayawon
# --------------------------------------

import pandas as pd
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import WorksheetNotFound
import json
import os

# 🧮Format float display to 2 decimal places
pd.options.display.float_format = "{:,.2f}".format

# 🔐Google Sheets API Authentication
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

json_creds = os.environ.get("GOOGLE_SHEETS_JSON")
creds_dict = json.loads(json_creds)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)

# 📥Load Form Responses
sheet = client.open("Superstore Orders").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# 🧼Rename and clean columns
df.columns = ["time_stamp", "customer_name", "product", "quantity", "region"]
df["time_stamp"] = pd.to_datetime(df["time_stamp"], errors="coerce")
df["order_date"] = df["time_stamp"].dt.date.astype(str)
df["order_time"] = df["time_stamp"].dt.time.astype(str)
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
df["customer_name"] = df["customer_name"].astype(str).str.strip()

# 🔤Compound name keywords (surname or middle name)
compound_keywords = {
    "del", "dela", "de", "van", "von", "san", "santa",
    "bin", "ibn", "da", "di", "la", "le", "mc", "mac"
}

# Middle name to initials (e.g., De Guzman → D.G.)
def extract_initials(name):
    initials = re.findall(r'\b([A-Za-z])[A-Za-z]*\.?', name)
    return '.'.join(i.upper() for i in initials) + '.' if initials else ''

# Parse full name from right: surname > middle > given
def parse_full_name(full_name):
    parts = full_name.strip().split()
    if not parts:
        return pd.Series(["", "", ""])

    # Step 1: Detect compound surname
    surname = parts[-1]
    remaining = parts[:-1]
    if len(remaining) >= 1 and remaining[-1].lower() in compound_keywords:
        surname = remaining[-1] + " " + surname
        remaining = remaining[:-1]

    # Step 2: Detect middle name or initials
    middle_name = ""
    given_name = ""

    if remaining:
        last = remaining[-1]
        # Format: D.G. or D. or DG
        if re.fullmatch(r"([A-Za-z]{1,2}\.?)|([A-Za-z]{1}\.[A-Za-z]{1}\.?)", last):
            middle_name = last
            given_name = " ".join(remaining[:-1])
        elif len(remaining) >= 2 and remaining[-2].lower() in compound_keywords:
            # Compound middle name (e.g., De Guzman)
            middle_name = " ".join(remaining[-2:])
            given_name = " ".join(remaining[:-2])
        else:
            # Single middle word
            middle_name = last
            given_name = " ".join(remaining[:-1])

    middle_initials = extract_initials(middle_name)

    return pd.Series([
        given_name.title().strip(),
        middle_initials,
        surname.title().strip()
    ])

# Apply name parsing
df[["given_name", "middle_name", "surname"]] = df["customer_name"].apply(parse_full_name)

# 🧽Standardize text columns
for col in ["given_name", "middle_name", "surname", "product", "region"]:
    df[col] = df[col].astype(str).str.strip().str.title()

# 📦Load Product Catalog
product_sheet_name = "Product_Prices"
try:
    product_sheet = client.open("Superstore Orders").worksheet(product_sheet_name)
except WorksheetNotFound:
    print(f"❌ Worksheet '{product_sheet_name}' not found.")
    for s in client.open("Superstore Orders").worksheets():
        print("Available sheet:", s.title)
    raise SystemExit("❗ Please check your worksheet name.")

product_data = product_sheet.get_all_records()
product_df = pd.DataFrame(product_data)
product_df["product_name"] = product_df["product_name"].astype(str).str.strip().str.title()
product_df["cost"] = product_df["cost"].replace(r'[$,]', '', regex=True).astype(float).round(2)
product_df["selling_price"] = product_df["selling_price"].replace(r'[$,]', '', regex=True).astype(float).round(2)

# 🔗Merge Order Data with Product Info
df = df.merge(product_df, how="left", left_on="product", right_on="product_name")

df["total_cost"] = (df["cost"] * df["quantity"]).round(2)
df["total_sales"] = (df["selling_price"] * df["quantity"]).round(2)
df["profit"] = (df["total_sales"] - df["total_cost"]).round(2)

# 🧾Final Column Order
df = df[[ 
    "order_date", "order_time",
    "surname", "given_name", "middle_name",
    "product", "product_id", "quantity", "region",
    "cost", "selling_price", "total_cost", "total_sales", "profit"
]]

# 🔄 Replace NaNs with 0.0 to ensure numeric columns stay numeric
df["quantity"] = df["quantity"].fillna(0).astype(int)

# Format monetary columns as $x,xxx.xx
currency_cols = ["cost", "selling_price", "total_cost", "total_sales", "profit"]
for col in currency_cols:
    df[col] = df[col].fillna(0.0).astype(float).map("${:,.2f}".format)


# 💾Export to Google Sheets
output_sheet_name = "Cleaned_Data"
workbook = client.open("Superstore Orders")

try:
    output_sheet = workbook.worksheet(output_sheet_name)
except WorksheetNotFound:
    print("🆕 Creating worksheet:", output_sheet_name)
    output_sheet = workbook.add_worksheet(title=output_sheet_name, rows=1000, cols=20)

output_sheet.clear()
output_sheet.update([df.columns.values.tolist()] + df.values.tolist())

print(f"\n✅ Data successfully written to '{output_sheet_name}' worksheet in 'Superstore Orders'.")
