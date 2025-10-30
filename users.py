import json
import os
import getpass  # hides password input

DATA_FILE = "data/users.json"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def create_user():
    users = load_users()
    username = input("Enter new username: ").strip()
    if username in users:
        print("❌ Username already exists!")
        return
    password = getpass.getpass("Enter password: ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        print("❌ Passwords do not match!")
        return
    users[username] = password
    save_users(users)
    print(f"✅ User '{username}' created successfully!")

def login():
    users = load_users()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    if username in users and users[username] == password:
        print(f"✅ Welcome, {username}!")
        return True
    else:
        print("❌ Invalid username or password!")
        return False
