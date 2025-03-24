from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Configuration (Replace with your actual credentials)
MONGO_URI = "mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority"  # Replace
DATABASE_NAME = "travel_db"

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]  # Access the database
    print("Connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None # Set db to None if connection fails

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    """Serializes a MongoDB document for JSON output."""
    doc['_id'] = str(doc.get('_id'))  #Safely access _id, if missing returns None
    return doc

# API Routes
@app.route('/')
def index():
    """Renders the index.html template with data from MongoDB."""
    if db:
        # Fetch data from MongoDB collections
        destinations = [serialize_doc(doc) for doc in db.destinations.find({})]  # Convert cursor to list
        deals = [serialize_doc(doc) for doc in db.deals.find({})]  # Fetch all deals
        popular_packages = [serialize_doc(doc) for doc in db.popular_packages.find({})]

        return render_template(
            'index.html',
            destinations=destinations,
            deals=deals,
            popular_packages=popular_packages
        )
    else:
        return "<h1>Error: Could not connect to the database.</h1>"



@app.route('/api/destinations')
def get_destinations():
    """Returns all destinations as JSON, with optional filtering by country."""
    if db:
        country = request.args.get('country')  # Get 'country' query parameter
        query = {}  # Empty query initially

        if country:
            query['country'] = country  # Add country filter if provided

        destinations = [serialize_doc(doc) for doc in db.destinations.find(query)]
        return jsonify(destinations)
    else:
        return jsonify({"error": "Could not connect to database"}), 500 # Return error code

@app.route('/api/deals')
def get_deals():
    """Returns all deals as JSON."""
    if db:
        deals = [serialize_doc(doc) for doc in db.deals.find({})]
        return jsonify(deals)
    else:
        return jsonify({"error": "Could not connect to database"}), 500


@app.route('/api/popular_packages')
def get_popular_packages():
    """Returns all popular packages as JSON."""
    if db:
        popular_packages = [serialize_doc(doc) for doc in db.popular_packages.find({})]
        return jsonify(popular_packages)
    else:
        return jsonify({"error": "Could not connect to database"}), 500


if __name__ == '__main__':
    app.run(debug=True) 