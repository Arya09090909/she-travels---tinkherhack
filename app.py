from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    with sqlite3.connect("she_travels.db") as conn:
        cursor = conn.cursor()

        # Create Users Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            bio TEXT,
                            instagram TEXT,
                            facebook TEXT,
                            twitter TEXT,
                            location TEXT,
                            profile_pic TEXT)''')

        # Create Activities Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS activities (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            description TEXT NOT NULL,
                            date TEXT NOT NULL,
                            FOREIGN KEY(user_id) REFERENCES users(id))''')

        # Create Explore Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS explore (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            category TEXT NOT NULL,
                            name TEXT NOT NULL,
                            description TEXT NOT NULL)''')

        # Insert Dummy Activities Data (Only if table is empty)
        cursor.execute("SELECT COUNT(*) FROM activities")
        if cursor.fetchone()[0] == 0:
            activities_data = [
                (1, "Visited Sunset Gardens for a peaceful evening", "2025-02-07"),
                (1, "Had lunch at The Grand Cafe – amazing coffee!", "2025-02-07"),
                (1, "Booked a stay at Blue Lagoon Resort for the weekend", "2025-02-06"),
                (1, "Helped a traveler find transport via City Taxi Services", "2025-02-06"),
                (1, "Met a travel buddy and explored Spice Heaven for dinner", "2025-02-05"),
                (1, "Attended a local event at Community Cultural Center", "2025-02-04"),
                (1, "Hosted a traveler from Bangalore and shared travel tips", "2025-02-03"),
                (1, "Explored Mountain View Trek – breathtaking views!", "2025-02-02"),
                (1, "Took a bike rental to explore the old city streets", "2025-02-01"),
                (1, "Booked a budget-friendly hostel near the city center", "2025-01-31")
            ]
            cursor.executemany("INSERT INTO activities (user_id, description, date) VALUES (?, ?, ?)", activities_data)

        # Insert Explore Data Only if Table is Empty
        cursor.execute("SELECT COUNT(*) FROM explore")
        if cursor.fetchone()[0] == 0:
            explore_data = [
                ('food', 'The Grand Cafe', 'A cozy place for coffee and snacks'),
                ('food', 'Spice Heaven', 'Authentic Indian dishes with great ambiance'),
                ('travel_spots', 'Sunset Gardens', 'A beautiful place to relax and enjoy nature'),
                ('transport', 'City Taxi Services', 'Affordable and safe taxi rides in the city'),
                ('stay', 'Blue Lagoon Resort', 'Luxurious stay with scenic views')
            ]
            cursor.executemany("INSERT INTO explore (category, name, description) VALUES (?, ?, ?)", explore_data)

        conn.commit()  # Save changes to the database

init_db()

# Database Connection Function
def get_db_connection():
    conn = sqlite3.connect("she_travels.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-style row access
    return conn

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/activities')
def activities():
    return render_template('activities.html')

@app.route('/food')
def food_page():
    return render_template('food.html')

@app.route('/travel_spots')
def travel_page():
    return render_template('travel_spots.html')

@app.route('/transport')
def transport_page():
    return render_template('transport.html')

@app.route('/stay')
def stay_page():
    return render_template('stay.html')

@app.route('/messages')
def messages():
    return render_template('messages.html')

# Fetch Explore Data (with optional category filter)
@app.route('/get_explore_data', methods=['GET'])
def get_explore_data():
    category = request.args.get('category', None)  # Get category from query parameter
    conn = get_db_connection()
    cursor = conn.cursor()

    if category:
        cursor.execute("SELECT category, name, description FROM explore WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT category, name, description FROM explore")

    explore_items = cursor.fetchall()
    conn.close()

    explore_list = [{"category": item["category"], "name": item["name"], "description": item["description"]} for item in explore_items]
    return jsonify(explore_list)

# ✅ Chat Route - FIXED
@app.route('/chat/<username>')
def chat(username):
    return render_template('chat.html', username=username.replace('_', ' '))

# ✅ Profile Route - FIXED (Now Properly Placed)
@app.route('/profile/<username>')
def profile(username):
    # Convert back to a proper name format
    formatted_username = username.replace('_', ' ')

    # Fetch user details from the database (assuming 'users' table exists)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (formatted_username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template('profile.html', user=user)
    else:
        return "User profile not found", 404

# Fetch Activities
@app.route('/get_activities', methods=['GET'])
def get_activities():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, description, date FROM activities ORDER BY date DESC")
    activities = cursor.fetchall()
    conn.close()

    activity_list = [{"id": act["id"], "user_id": act["user_id"], "description": act["description"], "date": act["date"]} for act in activities]
    return jsonify(activity_list)

# Run Flask App
if __name__ == '__main__':
    print("🚀 Flask is running...")  # Debugging message
    app.run(debug=True)
