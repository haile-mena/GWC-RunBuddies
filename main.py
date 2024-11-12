import random
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_login import LoginManager, login_required, current_user, UserMixin, login_user, logout_user
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Specify the login route

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('myDatabase.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return User(user['id'], user['username'], user['email'])
    return None

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('myDatabase.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                      (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            user_obj = User(user['id'], user['username'], user['email'])
            login_user(user_obj)
            session['username'] = username
            return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    return render_template('index.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('signup.html', error=False)
    
    if request.method == 'POST':
        user_id = random.randint(1000000000, 9999999999)
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if user exists
        exists, field = check_existing_user(username, email)
        if exists:
            return render_template('signup.html', 
                                 error=True, 
                                 message=f"This {field} is already taken")
        
        conn = sqlite3.connect('myDatabase.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)", 
                      (user_id, username, email, password))
        conn.commit()
        conn.close()
        
        session['username'] = username
        user = User(user_id, username, email)
        login_user(user)
        return render_template('survey.html')

# Basic routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/contact')
def contact():
    return 'This is the contact page'

# Dashboard routes
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/api/user-profile')
@login_required
def get_user_profile():
    conn = sqlite3.connect('myDatabase.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (session['username'],))
    user = cursor.fetchone()
    conn.close()
    
    return jsonify({
        "username": user['username'],
        "email": user['email']
    })

@app.route('/api/matches')
@login_required
def get_matches():
    # TODO: Replace with actual database query
    matches = [
        {"id": 1, "name": "Sarah", "age": 28, "match_percentage": 85},
        {"id": 2, "name": "Mike", "age": 31, "match_percentage": 78},
        {"id": 3, "name": "Emma", "age": 26, "match_percentage": 92}
    ]
    return jsonify({"matches": matches})

@app.route('/api/runs')
@login_required
def get_runs():
    # TODO: Replace with actual database query
    runs = [
        {"date": "2024-03-15", "distance": "5.2km", "time": "28:30"},
        {"date": "2024-03-17", "distance": "8.1km", "time": "45:15"},
        {"date": "2024-03-20", "distance": "4.5km", "time": "24:45"}
    ]
    return jsonify({"runs": runs})

@app.route('/api/messages')
@login_required
def get_messages():
    # TODO: Replace with actual database query
    messages = [
        {"from": "Sarah", "content": "Hey! How's your running going?", 
         "timestamp": "2024-03-20 14:30"},
        {"from": "Mike", "content": "Want to join my running group?", 
         "timestamp": "2024-03-19 16:45"}
    ]
    return jsonify({"messages": messages})

def check_existing_user(username, email):
    conn = sqlite3.connect('myDatabase.db')
    cursor = conn.cursor()
    
    if username:
        cursor.execute('SELECT 1 FROM users WHERE username = ? LIMIT 1', (username,))
        if cursor.fetchone():
            conn.close()
            print('username is taken')
            return True, 'username'
            
    if email:
        cursor.execute('SELECT 1 FROM users WHERE email = ? LIMIT 1', (email,))
        if cursor.fetchone():
            conn.close()
            print('email is taken')
            return True, 'email'
    
    conn.close()
    return False, None

# Add these routes to your main.py

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        conn = sqlite3.connect('myDatabase.db')
        cursor = conn.cursor()
        
        # Get user_id from session
        cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
        user_id = cursor.fetchone()[0]
        
        # Insert basic preferences
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences 
            (user_id, age, gender, running_level, preferred_distance, 
             running_frequency, preferred_time, location, goals, bio)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            request.form.get('age'),
            request.form.get('gender'),
            request.form.get('running_level'),
            request.form.get('preferred_distance'),
            request.form.get('running_frequency'),
            request.form.get('preferred_time'),
            request.form.get('location'),
            request.form.get('goals'),
            request.form.get('bio')
        ))
        
        # Insert running preferences
        cursor.execute("""
            INSERT OR REPLACE INTO running_preferences 
            (user_id, preferred_pace, race_participation, 
             preferred_terrain, group_runs, cross_training)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            request.form.get('preferred_pace'),
            request.form.get('race_participation') == 'true',
            request.form.get('preferred_terrain'),
            request.form.get('group_runs') == 'true',
            request.form.get('cross_training')
        ))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('dashboard'))
        
    return render_template('survey.html')

@app.route('/api/user-settings')
@login_required
def get_user_settings():
    conn = sqlite3.connect('myDatabase.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get user_id
    cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
    user_id = cursor.fetchone()['id']
    
    # Get preferences
    cursor.execute("""
        SELECT up.*, rp.*
        FROM user_preferences up
        LEFT JOIN running_preferences rp ON up.user_id = rp.user_id
        WHERE up.user_id = ?
    """, (user_id,))
    
    preferences = cursor.fetchone()
    conn.close()
    
    if preferences:
        return jsonify({
            "basic_preferences": {
                "age": preferences['age'],
                "gender": preferences['gender'],
                "running_level": preferences['running_level'],
                "preferred_distance": preferences['preferred_distance'],
                "running_frequency": preferences['running_frequency'],
                "preferred_time": preferences['preferred_time'],
                "location": preferences['location'],
                "goals": preferences['goals'],
                "bio": preferences['bio']
            },
            "running_preferences": {
                "preferred_pace": preferences['preferred_pace'],
                "race_participation": preferences['race_participation'],
                "preferred_terrain": preferences['preferred_terrain'],
                "group_runs": preferences['group_runs'],
                "cross_training": preferences['cross_training']
            }
        })
    
    return jsonify({"error": "No preferences found"}), 404

@app.route('/api/user-settings', methods=['PUT'])
@login_required
def update_user_settings():
    data = request.get_json()
    
    conn = sqlite3.connect('myDatabase.db')
    cursor = conn.cursor()
    
    # Get user_id
    cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
    user_id = cursor.fetchone()[0]
    
    try:
        # Update basic preferences
        if 'basic_preferences' in data:
            prefs = data['basic_preferences']
            cursor.execute("""
                UPDATE user_preferences 
                SET age=?, gender=?, running_level=?, preferred_distance=?,
                    running_frequency=?, preferred_time=?, location=?,
                    goals=?, bio=?, updated_at=CURRENT_TIMESTAMP
                WHERE user_id=?
            """, (
                prefs.get('age'),
                prefs.get('gender'),
                prefs.get('running_level'),
                prefs.get('preferred_distance'),
                prefs.get('running_frequency'),
                prefs.get('preferred_time'),
                prefs.get('location'),
                prefs.get('goals'),
                prefs.get('bio'),
                user_id
            ))
        
        # Update running preferences
        if 'running_preferences' in data:
            prefs = data['running_preferences']
            cursor.execute("""
                UPDATE running_preferences 
                SET preferred_pace=?, race_participation=?,
                    preferred_terrain=?, group_runs=?,
                    cross_training=?, updated_at=CURRENT_TIMESTAMP
                WHERE user_id=?
            """, (
                prefs.get('preferred_pace'),
                prefs.get('race_participation'),
                prefs.get('preferred_terrain'),
                prefs.get('group_runs'),
                prefs.get('cross_training'),
                user_id
            ))
        
        conn.commit()
        return jsonify({"message": "Settings updated successfully"})
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
        
    finally:
        conn.close()

@app.route('/api/chat/<int:match_id>', methods=['GET'])
@login_required
def get_chat_messages(match_id):
    conn = sqlite3.connect('myDatabase.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get current user's ID
    cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
    user_id = cursor.fetchone()['id']
    
    # Get chat messages
    cursor.execute("""
        SELECT m.*, u.username as sender_name
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id = ? AND m.receiver_id = ?)
        OR (m.sender_id = ? AND m.receiver_id = ?)
        ORDER BY m.timestamp ASC
    """, (user_id, match_id, match_id, user_id))
    
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({"messages": messages})

@app.route('/api/chat/<int:match_id>', methods=['POST'])
@login_required
def send_message(match_id):
    data = request.get_json()
    message_content = data.get('message')
    
    conn = sqlite3.connect('myDatabase.db')
    cursor = conn.cursor()
    
    # Get sender ID
    cursor.execute("SELECT id FROM users WHERE username = ?", (session['username'],))
    sender_id = cursor.fetchone()[0]
    
    try:
        cursor.execute("""
            INSERT INTO messages (sender_id, receiver_id, content, timestamp)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (sender_id, match_id, message_content))
        
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)