import pandas as pd
import sqlite3

# Read the CSV file into a DataFrame
csv_file_path = 'dataset/REVIEWS_TABLE_final.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path, encoding='latin1')



# Connect to SQLite database (this will create a new database if it doesn't exist)
db_path = 'instance/users.db'  # Replace with the path to your SQLite database file
conn = sqlite3.connect(db_path)

# Define the data types for each column
dtype_mapping = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'user_id': 'TEXT',
    'restaurant_id': 'TEXT',
    'menu_item_id': 'TEXT',
    'reviews': 'TEXT',
    'date': 'DATE',
    'sentiment': 'INT'


}

# Write the DataFrame to the SQLite database with specified data types
table_name = 'reviews'  # Replace with the desired table name
df.to_sql(table_name, conn, index=False, if_exists='replace', dtype=dtype_mapping)

# Close the database connection
conn.close()
