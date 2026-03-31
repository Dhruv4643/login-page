from flask import Flask, request, render_template, redirect, url_for
import json
import os

app = Flask(__name__)

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        if not username or not password:
            message = "❌ Please fill in both fields."
        else:
            users = load_users()
            if username in users:
                message = "❌ That username is already taken. Try another."
            else:
                users[username] = password
                save_users(users)
                message = "✅ Registered successfully! You can now log in."
    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        users = load_users()
        if username in users and users[username] == password:
            # ✅ Login success → go to welcome page
            return redirect(url_for("welcome", username=username))
        else:
            message = "❌ Wrong username or password. Please try again."
    return render_template("index.html", message=message)

@app.route("/welcome/<username>")
def welcome(username):
    return render_template("welcome.html", username=username)

if __name__ == "__main__":
    app.run(debug=True)