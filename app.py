from flask import Flask, render_template, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = 'travel_db'

# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
top_destinations_collection = db['top_destinations']

@app.route('/api/destinations')
def get_destinations():
    """
    API endpoint to retrieve all destinations from the database.
    """
    try:
        destinations = list(top_destinations_collection.find({}, {'_id': 0}))  # Fetch all, exclude _id
        return jsonify(destinations)  # Return data as JSON
    except Exception as e:
        print(f"Error fetching destinations: {e}")
        return jsonify({'error': 'Failed to retrieve destinations'}), 500 # Return error status

@app.route('/')
def index():
    """
    Renders the index.html template. The destinations data will be fetched
    dynamically using JavaScript.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)