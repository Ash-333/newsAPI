from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

app = Flask(__name__)

# Initialize MongoDB Atlas connection
client = MongoClient("mongodb+srv://akamat62:apple23@cluster0.czjhohp.mongodb.net/?retryWrites=true&w=majority")

# Specify the MongoDB database and collection
db = client['News']
collection = db['items']

tele_url = "http://telegraphnepal.com/feed/"  # Replace with the URL of your RSS feed
online_url = "http://english.onlinekhabar.com/feed/"  # Replace with the URL of your RSS feed

# Function to fetch data from a given URL
def fetch_data(url):
    try:
        # Fetch XML data from the URL
        response = requests.get(url)
        if response.status_code == 200:
            xml_data = response.text

            # Parse the XML
            root = ET.fromstring(xml_data)

            # Iterate through <item> elements and prepare new items
            for item_elem in root.findall('.//item'):
                title = item_elem.find('title').text
                
                link = item_elem.find('link').text
                description = item_elem.find('description').text

                # Check if the item with the same link already exists in the collection
                existing_item = collection.find_one({'link': link})
                if existing_item is None:
                    print(f"fetched:{link}")
                    # Extract image URL from <content:encoded> and <img> elements
                    encoded_content = item_elem.find('content:encoded', namespaces={'content': 'http://purl.org/rss/1.0/modules/content/'})
                    if encoded_content is not None:
                        cdata_content = encoded_content.text.strip() if encoded_content.text else ""
                        soup = BeautifulSoup(cdata_content, 'html.parser')
                        img_tags = soup.find_all('img')
                        img_src = img_tags[0]['src'] if img_tags else None

                    # Create a dictionary for each new item
                    new_item_data = {
                        'title': title,
                        'link': link,
                        'description': description,
                        'img_url': img_src,
                    }

                    # Insert the new item into the collection
                    collection.insert_one(new_item_data)

    except Exception as e:
        print("Error fetching or parsing data:", str(e))

# Create a BackgroundScheduler to periodically update data
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data, 'interval', minutes=1, args=[tele_url])
scheduler.add_job(fetch_data, 'interval', minutes=1, args=[online_url])
scheduler.start()

# ...

@app.route('/items', methods=['GET'])
def get_items():
    # Retrieve all data from the MongoDB Atlas collection
    items = collection.find()

    # Create a list to store the retrieved items
    item_list = []

    # Iterate through the items and format them as a list of dictionaries
    for item in items:
        item_data = {
            'title': item['title'],
            'link': item['link'],
            'description': item['description'],
            'img_url': item['img_url']
        }
        item_list.append(item_data)

    # Return the list of items as JSON
    return jsonify(item_list)

if __name__ == '__main__':
    app.run(debug=True)
