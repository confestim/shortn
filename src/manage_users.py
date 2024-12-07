import sqlite3
import argparse
from werkzeug.security import generate_password_hash, check_password_hash
import getpass
import sys

DATABASE = 'database.db'

# Function to initialize the database (if not already done)
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

# Function to add a new user
def add_user(username, password):
    hashed_password = generate_password_hash(password)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            print(f"User '{username}' created successfully.")
        except sqlite3.IntegrityError:
            print(f"Error: User '{username}' already exists.")

# Function to delete a user
def delete_user(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully.")
        else:
            print(f"Error: User '{username}' not found.")

# Function to list all users
def list_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username FROM users')
        users = cursor.fetchall()
        if users:
            print("Users:")
            for user in users:
                print(f" - ID: {user[0]}, Username: {user[1]}")
        else:
            print("No users found.")

# CLI argument parser
def main():
    parser = argparse.ArgumentParser(description="User management CLI for the Flask app.")
    parser.add_argument('command', choices=['add', 'delete', 'list', 'init'], help="Command to execute.")
    parser.add_argument('--username', help="Username of the user.")
    args = parser.parse_args()

    # Execute the appropriate function based on the command
    if args.command == 'init':
        init_db()
        print("Database initialized.")
    elif args.command == 'add':
        user = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        verify = getpass.getpass("Re-enter password: ")
        if password != verify:
            print("Error: Passwords do not match.")
            sys.exit(1)
        add_user(user, password)
    elif args.command == 'delete':
        if not args.username:
            print("Error: --username is required for 'delete' command.")
        else:
            delete_user(args.username)
    elif args.command == 'list':
        try:
            list_users()
        except sqlite3.OperationalError:
            print("Error: Database not initialized. Run 'init' command first.")
    else:
        print("Invalid command. Use --help for usage information.")

if __name__ == '__main__':
    main()
