from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
from datetime import datetime
import uuid
import random
import string
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)


class reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    restaurant_id = db.Column(db.String(50), nullable=False)
    menu_item_id = db.Column(db.String(50), nullable=False)
    reviews = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    sentiment =db.Column(db.Integer)

class restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    owner_mgr_id = db.Column(db.String(15), nullable=False)
    restaurant_rating = db.Column(db.Float, nullable=False)

class menu_item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.String(20), nullable=False)
    restaurant_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(15), nullable=False)
    menu_item_rating = db.Column(db.Float, nullable=False)

class all_menu_items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.String(20), nullable=False)
    menu_item_name = db.Column(db.String(50), nullable=False)

@app.route('/receive', methods=['POST'])
def receive_data():
    try: 
        data = request.get_json()
        received_data = data.get('data', '')

        print(f"Received data from Angular: {received_data}")
        firstName = received_data.get("firstName", "")
        lastName = received_data.get("lastName", "")
        username = received_data.get("username", "")
        password = received_data.get("password", "")

        print("password",password)
        salt = bcrypt.gensalt(rounds = 12)
        print("salt: ", salt)

        encoded = password.encode('utf-8')
        print("encoded: ", encoded)
        hashed = bcrypt.hashpw(encoded, salt)
        print("hashed: ", hashed)

        # Check if the username already exists
        if User.query.filter_by(username=username.lower()).first():
            return jsonify({"error": "Username already exists"}), 400

        # Create a new user record in the database
        new_user = User(firstname=firstName, lastname=lastName, username=username.lower(), hashed_password=hashed)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Data received and stored successfully", "firstname": firstName})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    received_data = data.get('data', '')
    print(f"Received data from Angular: {received_data}")
    

    username = received_data.get("username", "")
    password = received_data.get("password", "")

    user = User.query.filter_by(username=username.lower()).first()
    
    if user:
        print(f"Stored Password: {user.hashed_password}")
        print(f"Provided Password: {password}")

        decode = bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

        print("decoded: ", decode)

        if decode:
            return jsonify({"message": "Login successful!", "firstname":user.firstname})

    return jsonify({"error": "Invalid username or password"}), 401


@app.route('/get_restaurants', methods=['GET'])
def get_restaurants():
    # Retrieve restaurant data from the database
    restaurants = restaurant.query.all()

    # Serialize the data to JSON
    restaurant_data = []
    for r in restaurants:
        restaurant_data.append({
            'restaurant_id': r.restaurant_id,
            'name': r.name,
            'location': r.location,
            'owner_mgr_id': r.owner_mgr_id
        })

    return jsonify({'restaurants': restaurant_data})


@app.route('/get_menu_items', methods=['POST'])
def get_menu_items():
    data = request.get_json()
    restaurant_id = data.get('restaurantId', '')

    print(restaurant_id)
    # Your logic to fetch menu items for the specified restaurant_id
    menu_items = menu_item.query.filter_by(restaurant_id=restaurant_id).all()

    # Serialize the data to a list of dictionaries
    menu_items_data = []
    for item in menu_items:
        menu_items_data.append({
            'menu_item_id': item.menu_item_id,
            'name': item.name,
            'description': item.description,
            'price': item.price
        })
    

    return jsonify({'menuItems': menu_items_data})


print("Data imported successfully!")

@app.route('/add_review', methods=['POST'])
def add_review():
    try:
        data = request.get_json()
        
        firstname = data.get('firstname', '')
        restaurant_id = data.get('restaurantId', '')
        menu_item_id = data.get('menuItemId', '')
        review_text = data.get('reviewText', '')
        date_str = data.get('date', '')

        date=datetime.strptime(date_str, '%m/%d/%Y')

        print(f"Received data for review - Firstname: {firstname}, "
              f"Restaurant ID: {restaurant_id}, Menu Item ID: {menu_item_id}, Review Text: {review_text}, Date: {date}")
        
        def generate_unique_user_id():
            while True:
                random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                user = reviews.query.filter_by(user_id=random_chars).first()
                if not user:
                    return random_chars

        # Example usage
        random_user_id = generate_unique_user_id()
        print("Random Unique User ID:", random_user_id)


        # Create a new user record in the database
        new_review = reviews(user_id=random_user_id, restaurant_id=restaurant_id, menu_item_id=menu_item_id, reviews=review_text,
            date=date, sentiment=None)
        db.session.add(new_review)
        db.session.commit()

        return jsonify({"message": "Review added successfully"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route('/get_reviews', methods=['POST'])
def get_reviews():
    try:
        data = request.get_json()
        restaurant_id = data.get('restaurantId', '')
        menu_item_id = data.get('menuItemId', '')

        # Your logic to fetch reviews for the specified restaurant_id and menu_item_id
        reviews = reviews.query.filter_by(restaurant_id=restaurant_id, menu_item_id=menu_item_id).all()

        # Serialize the reviews data to a list of dictionaries
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                'user_id': review.user_id,
                'review_text': review.reviews,
                'date': review.date,
                'sentiment': review.sentiment
            })

        return jsonify({'reviews': reviews_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500  


# ...

@app.route('/get_all_menu_items', methods=['GET'])
def get_all_menu_items():
    try:
        # Retrieve all menu items from the database
        all_menu_items_data = all_menu_items.query.all()

        # Serialize the data to a list of dictionaries
        menu_items_data = []
        for item in all_menu_items_data:
            menu_items_data.append({
                'menu_item_id': item.menu_item_id,
                'menu_item_name': item.menu_item_name
            })

        return jsonify({'allMenuItems': menu_items_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500

@app.route('/send_selected_menu_item', methods=['POST'])
def send_selected_menu_item():
    try:
        data = request.get_json()
        selected_menu_item = data.get('selectedMenuItem', '')

        # Your logic to handle the selected_menu_item
        print(f"Received selected menu item ID: {selected_menu_item}")

        # Add your additional logic here...
        query = text("""
            SELECT 
                m.menu_item_id, 
                m.name,
                m.restaurant_id, 
                restaurant.name AS restaurant_name,
                m.menu_item_rating, 
                (SELECT r.restaurant_rating FROM restaurant r WHERE r.restaurant_id = m.restaurant_id) AS restaurant_rating
                FROM 
                    menu_item m
                    inner join restaurant on m.restaurant_id = restaurant.restaurant_id
                WHERE 
                    m.menu_item_id = :selected_menu_item
                ORDER BY 
                    m.menu_item_rating DESC, restaurant_rating DESC
                LIMIT 3
        """)

        query_result = db.session.execute(query, {"selected_menu_item": selected_menu_item}).fetchall()
        print(query_result)

        result_data = []
        for row in query_result:
            result_data.append({
                'name': row.name,
                'restaurant_name': row.restaurant_name,
                'menu_item_rating': row.menu_item_rating,
                'restaurant_rating': row.restaurant_rating
            })
        

        return jsonify({"result": result_data})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": f"Internal Server Error: {e}"}), 500



if __name__ == '__main__':
    with app.app_context():
    # Create the database tables before running the app
        db.create_all()
    app.run(port=5000)

