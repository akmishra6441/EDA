import pandas as pd
from sqlalchemy import create_engine, text

# --- MySQL Connection Details ---
user = "root"           # your MySQL username
password = "password"  # your MySQL password
host = "localhost"      # or "127.0.0.1"
database = "sales_db"   # database name to create/use

# Create a connection (without database first, to create it)
root_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/")

# Create database if it doesn't exist
with root_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database};"))
    print(f"Database '{database}' created or already exists.")

# Reconnect to the new database
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# --- File mapping: Table name → Excel file ---
files = {
    "sales_team": "Sales_Team_sheet.xlsx",
    "region": "Region_Sheet.xlsx",
    "product": "Product_Sheet.xlsx",
    "store": "Store_Location.xlsx",
    "customer": "Customer_Sales_Data.xlsx",
    "sales": "US_Sales Data.xlsx"
}

# --- Load and Insert Data ---
for table_name, file_path in files.items():
    df = pd.read_excel(file_path)
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    print(f"Table '{table_name}' created and data inserted.")

print("\nAll Excel files loaded into MySQL successfully!")

# --- Optional: Add Primary and Foreign Keys ---
with engine.connect() as conn:
    # Add primary keys (adjust as per your schema)
    conn.execute(text("""
        ALTER TABLE sales_team ADD PRIMARY KEY (_SalesTeamID);
    """))
    conn.execute(text("""
        ALTER TABLE region ADD PRIMARY KEY (StateCode);
    """))
    conn.execute(text("""
        ALTER TABLE product ADD PRIMARY KEY (_ProductID);
    """))
    conn.execute(text("""
        ALTER TABLE store ADD PRIMARY KEY (_StoreID);
    """))
    conn.execute(text("""
        ALTER TABLE customer ADD PRIMARY KEY (_CustomerID);
    """))
    conn.execute(text("""
        ALTER TABLE sales ADD PRIMARY KEY (OrderNumber);
    """))

    # Add Foreign Keys to link sales with other tables
    conn.execute(text("""
        ALTER TABLE sales 
        ADD CONSTRAINT fk_sales_team FOREIGN KEY (_SalesTeamID) REFERENCES sales_team(_SalesTeamID),
        ADD CONSTRAINT fk_customer FOREIGN KEY (_CustomerID) REFERENCES customer(_CustomerID),
        ADD CONSTRAINT fk_product FOREIGN KEY (_ProductID) REFERENCES product(_ProductID),
        ADD CONSTRAINT fk_store FOREIGN KEY (_StoreID) REFERENCES store(_StoreID);
    """))

print("Primary keys and foreign keys added successfully!")
