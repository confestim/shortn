from flask import Flask, request, redirect, url_for, render_template, flash, session, jsonify
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'super secret key' # FIXME: CHANGE THISSSSSSSSS!

# Database initialization
DATABASE = 'database.db'
if not os.path.exists(DATABASE):
    raise FileNotFoundError(f"Database file not found. Run `python manage_users.py init` to create it.")

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS redirects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dest_link TEXT NOT NULL,
                custom_link TEXT UNIQUE
            )
        ''')
        conn.commit()

# Helper function to interact with the database
def query_db(query, args=(), one=False):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        rv = cursor.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

@app.route('/redirects', methods=['GET', 'POST'])
def redirects_list():
    if 'username' not in session:  # Ensure the user is logged in
        return redirect(url_for('login'))

    if request.method == 'POST':  # Handle deletion
        redirect_id = request.form.get('redirect_id')
        if redirect_id:
            query_db('DELETE FROM redirects WHERE id = ?', (redirect_id,))
            flash('Redirect deleted successfully!')
            return redirect(url_for('redirects_list'))

    # Fetch all active redirects
    redirects = query_db('SELECT id, dest_link, custom_link FROM redirects')
    return render_template('redirects.html', redirects=redirects)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('form'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('form'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def verify_link(link:str) -> bool:
    if not link.startswith('http://') and not link.startswith('https://'):
        link = 'http://' + link
    reg = r'^(https?:\/\/)(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})(:\d+)?(\/[a-zA-Z0-9@:%_\+.~#?&//=]*)?$'
    
    return bool(re.match(reg, link))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        dest_link = request.form['dest_link']
        if not verify_link(dest_link):
            flash('Invalid URL. Make sure it starts with http:// or https://')
            return render_template('nohack.html')
        
        custom_link = request.form.get('custom_link', None)

        try:
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO redirects (dest_link, custom_link) VALUES (?, ?)', 
                                (dest_link, custom_link))
                conn.commit()
                flash('Redirect created successfully!')
                return render_template('success.html', link=custom_link if custom_link else f"/r/{cursor.lastrowid}")
        except sqlite3.IntegrityError:
            flash('Custom link already exists. Try another.')
    
    # return render_template('form.html', 
    #  return template with user logged in flag
    return render_template('form.html', user_logged_in=True)

@app.route('/r/<custom_link>')
def redirect_to_custom(custom_link):
    with sqlite3.connect(DATABASE) as conn:
        if result := query_db('SELECT dest_link FROM redirects WHERE custom_link = ?', (custom_link,), one=True):
            # Redirect to external link
            return redirect(result[0])
        else:
            return 'Redirect not found', 404

# For testing purpose, use a method to create users
@app.route('/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                return 'User created successfully!'
            except sqlite3.IntegrityError:
                return 'User already exists.'


# 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
