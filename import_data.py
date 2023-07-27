import os
import pandas as pd
import couchdb

couchdb_url = 'http://127.0.0.1:5984'
db_name = 'jenkins_retails'
username = 'admin'
password = '654321'

couch = couchdb.Server(couchdb_url)
couch.resource.credentials = (username, password)

if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

# Get the current working directory
current_directory = os.getcwd()

# Combine the current directory with the Excel filename
excel_filename = 'Project2Data.xlsx'
excel_file_path = os.path.join(current_directory, excel_filename)

def handle_value(value):
    if pd.notna(value):
        return str(value)  # Convert to string to handle the changed datatype
    else:
        return None

# Function to add the "Demand" field based on "Quantity" value
def calculate_demand(quantity):
    if quantity > 20:
        return "High"
    elif 12 <= quantity <= 20:
        return "moderate"
    else:
        return None  # No "Demand" field for quantities less than 12

# Reading the Excel file into a DataFrame
df = pd.read_excel(excel_file_path)

# Iterating through each row and create JSON objects for each record
records = []
for index, row in df.iterrows():
    record = {
        "StockCode": row['StockCode'],
        "Description": row['Description'],
        "Quantity": int(row['Quantity']),
        "Price": str(row['Price']), 
        "Country": row['Country']
    }

    # Add "CustomerID" field only if it exists in the Excel file
    if 'Customer ID' in df.columns:
        record['CustomerID'] = row['Customer ID']

    # Calculate and add the "Demand" field based on the "Quantity"
    if row['Quantity'] > 12:
        record['Demand'] = calculate_demand(row['Quantity'])

    # Save the record into CouchDB
    db.save(record)
