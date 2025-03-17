import sqlite3
from flask import Flask, request, render_template, jsonify, session, g, render_template_string

app = Flask(__name__)
app.secret_key = "verysecurekey"
DATABASE = "users.db"
HARD_CODED_API_KEY = "debug-access-1234"  # Hidden in frontend JS (bad practice)

def get_db():
    if not hasattr(g, "_database"):
        g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, "_database"):
        g._database.close()

# def init_db():
#     with app.app_context():
#         db = get_db()
#         db.executescript("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         );
#         INSERT OR IGNORE INTO users (username, password) VALUES 
#         ('admin', 'supersecret'),
#         ('user1', 'password123'),
#         ('pentester', 'exploiter');
#         """)
#         db.commit()

# init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return "Unauthorized", 401
    return render_template("dashboard.html", user=session["user"])

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()

    if user:
        session["user"] = username
        return jsonify({"status": "success", "redirect": "/dashboard"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route("/logout")
def logout():
    session.pop("user", None)
    return "Logged out."

# 🛑 **Hidden API Endpoint - Vulnerable to SSTI**
@app.route("/api/debug", methods=["POST"])
def debug():
    if request.headers.get("X-API-KEY") != HARD_CODED_API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    log_data = request.json.get("log", "No logs provided")
    
    # ⚠️ Vulnerable SSTI
    return render_template_string(f"<pre>Server Log: {log_data}</pre>")

if __name__ == "__main__":
    app.run(debug=True)

