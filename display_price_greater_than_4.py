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
    print("Database not found.")
    exit()

# Function to check if a document contains the "Demand" field
def has_demand_field(doc):
    return "Demand" in doc

# Function to display the records with price greater than 4
def display_records_with_price_greater_than_4():
    all_documents = db.view('_all_docs', include_docs=True)
    records_with_price_greater_than_4 = []
    for row in all_documents:
        doc = row.doc
        if 'Price' in doc:
            try:
                price = float(doc['Price'])
                if price > 4:
                    records_with_price_greater_than_4.append(doc)
            except ValueError:
                pass  # Skip the document if Price is not a valid float

    # Display the filtered records
    print("Records with price greater than 4 (4 excluded):")
    for record in records_with_price_greater_than_4:
        print(record)

# Call the function to display the filtered records
display_records_with_price_greater_than_4()
