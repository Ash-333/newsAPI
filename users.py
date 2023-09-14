from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB Atlas
try:
    client = MongoClient("mongodb+srv://akamat62:apple23@cluster0.n4myeha.mongodb.net/users?retryWrites=true&w=majority")
    db = client.get_database("users")
    users_collection = db.get_collection("users")

    print("DB connection id done")

except Exception as e:
    print(f"Error: {str(e)}")

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')

    if name and address:
        # Insert the user data into the MongoDB collection
        users_collection.insert_one({'name': name, 'address': address})
        return jsonify({'message': 'User added successfully'})
    else:
        return jsonify({'message': 'Invalid data. Please provide both name and address.'}), 400

@app.route('/get_user/<name>', methods=['GET'])
def get_user(name):
    user = users_collection.find_one({'name': name})
    if user:
        return jsonify({'name': user['name'], 'address': user['address']})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    all_users = list(users_collection.find({}, {'_id': False}))
    return jsonify({'users': all_users})

if __name__ == '__main__':
    app.run(debug=True)
