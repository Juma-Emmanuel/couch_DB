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

# Get all the documents from the database
all_documents = db.view('_all_docs', include_docs=True)

# Count the number of documents with the "Demand" field
documents_with_demand = sum(1 for row in all_documents if has_demand_field(row.doc))

# Total number of records in the database
total_records = len(all_documents)

# Number of records with the "Demand" field
records_with_demand = documents_with_demand

# Number of records without the "Demand" field
records_without_demand = total_records - records_with_demand

print(f"Total number of records: {total_records}")
print(f"Number of records with 'Demand' field: {records_with_demand}")
print(f"Number of records without 'Demand' field: {records_without_demand}")
