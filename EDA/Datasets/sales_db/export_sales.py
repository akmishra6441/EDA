import pandas as pd
from sqlalchemy import create_engine

# --- MySQL connection details (EDIT THESE) ---
user = "root"             # your MySQL username
password = "password"  # your MySQL password
host = "localhost"         # or "127.0.0.1"
database = "sales_db"      # your database name

# Connect to MySQL
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Load the full sales table (already merged data)
sales_df = pd.read_sql("SELECT * FROM sales", engine)

# Export to Excel
output_file = "Sales_Export.xlsx"
sales_df.to_excel(output_file, sheet_name="Sales_Data", index=False)

print(f"Export completed! File saved as {output_file}")
