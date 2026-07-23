from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = "event_data.db"


def get_db():
    return sqlite3.connect(DB)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def register():
    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, phone, gameid, time)
        VALUES (?, ?, ?, ?)
        """,
        (
            data.get("name", ""),
            data.get("phone", ""),
            data.get("gameid", ""),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})


@app.route("/api/users")
def users():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, phone, gameid, time FROM users"
    )

    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
