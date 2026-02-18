import sqlite3
import subprocess
import pickle
import base64

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
conn.execute("INSERT INTO users VALUES (1, 'admin', 'secret123')")
conn.commit()

def login(username, password):
    # INSECURE: SQL Injection - user input concatenated directly into query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    print(f"[DEBUG] Running query: {query}")
    result = conn.execute(query).fetchone()
    return result is not None

def ping_host(host):
    # INSECURE: Command Injection - user input passed to shell unsanitized
    output = subprocess.check_output("ping -c 1 " + host, shell=True)
    print(output.decode())

def load_profile(encoded_data):
    # INSECURE: Arbitrary code execution via pickle deserialization of user input
    raw = base64.b64decode(encoded_data)
    profile = pickle.loads(raw)
    print(f"Welcome, {profile.get('name', 'unknown')}!")

def main():
    print("=== Vulnerable App ===")
    action = input("Choose action (login / ping / profile): ").strip()

    if action == "login":
        u = input("Username: ")
        p = input("Password: ")
        print("Access granted!" if login(u, p) else "Access denied.")
    elif action == "ping":
        host = input("Enter hostname to ping: ")
        ping_host(host)
    elif action == "profile":
        data = input("Enter base64 profile data: ")
        load_profile(data)
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
