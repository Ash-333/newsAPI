from flask import Flask, jsonify
from pymongo import MongoClient
import xml.etree.ElementTree as ET
import requests
import schedule
import time

app = Flask(__name__)

# Initialize the MongoDB client
client = MongoClient("mongodb+srv://akamat62:apple23@cluster0.czjhohp.mongodb.net/News?retryWrites=true&w=majority")

# Select your database (replace 'mydb' with your database name)
db = client["News"]

# Create a collection (replace 'items' with your collection name)
items_collection = db["items"]

# URL of the XML feed
url = "https://english.onlinekhabar.com/feed"

# Function to update MongoDB data from XML
def update_data():
    response = requests.get(url)
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()

    for item_elem in root.findall(".//item"):
        title = item_elem.find("title").text
        link = item_elem.find("link").text
        description = item_elem.find("description").text
        img_src = item_elem.find(".//img").attrib["src"]

        item_document = {
            "title": title,
            "link": link,
            "description": description,
            "img_src": img_src
        }

        # Upsert the document based on the 'title' as a unique key
        items_collection.update_one({"title": title}, {"$set": item_document}, upsert=True)

        client.save()

# Schedule automatic updates every 10 minutes
schedule.every(10).minutes.do(update_data)

# Route to retrieve all items
@app.route('/items', methods=['GET'])
def get_items():
    items = list(items_collection.find({}))
    for item in items:
        item['_id'] = str(item['_id'])
    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)

    # Run the scheduled tasks in the background
    while True:
        schedule.run_pending()
        time.sleep(1)
