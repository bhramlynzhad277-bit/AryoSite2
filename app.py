from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

DB_FILE = "database.json"


def load_database():
    if not os.path.exists(DB_FILE):
        return []

    with open(DB_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_database(data):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    users = load_database()

    new_user = {
        "name": data.get("name", ""),
        "gameid": data.get("gameid", ""),
        "phone": data.get("phone", ""),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    users.append(new_user)
    save_database(users)

    return jsonify({
        "success": True,
        "message": "ثبت شد"
    })


@app.route("/api/users")
def users():
    return jsonify(load_database())


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
