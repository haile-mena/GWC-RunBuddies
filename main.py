# main.py
import random
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import datetime

#db = sqlite3.connect('myDatabase.db')


app = Flask(__name__)
app.secret_key = "secret"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/contact')
def contact():
    return 'This is the contact page'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('profile'))
    return render_template('login.html')

# user creates account - add to database
@app.route('/join', methods=['GET', 'POST'])
def join():
    #generate random user id - 10 digits
    user_id = random.randint(1000000000, 9999999999)

    if request.method == 'GET':
        return render_template('signup.html', error=False)
    if request.method == 'POST':
        #connect to database
        connect = sqlite3.connect('myDatabase.db')
        connect.row_factory = sqlite3.Row
        cursor = connect.cursor()
        
        session['username'] = request.form['username']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
            
            
            # add to database
            #cursor = db.cursor()
        cursor.execute("INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)", (user_id,session['username'], session['email'], session['password']))
        connect.commit()
        connect.close()
        #return redirect(url_for('profile'))
        return render_template('survey.html')

@app.route('/profile')
def profile():
    return 'This is the profile page'

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    return render_template('survey.html')

def check_existing_user(username=None, email=None):
    conn = sqlite3.connect('myDatabase.db')
    c = conn.cursor()
    
    if username:
        c.execute('SELECT 1 FROM users WHERE username = ? LIMIT 1', (username,))
        if c.fetchone():
            conn.close()
            return True, 'username'
            
    if email:
        c.execute('SELECT 1 FROM users WHERE email = ? LIMIT 1', (email,))
        if c.fetchone():
            conn.close()
            return True, 'email'
    
    conn.close()
    return False, None

if __name__ == '__main__':
    app.run(debug=True)
    