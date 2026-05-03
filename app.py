from flask import Flask, request, render_template, redirect, url_for
import sqlite3, os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

def get_db():
    return sqlite3.connect(db_path)

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"
        print(query)

        try:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                return redirect(url_for("dashboard"))
            else:
                message = "❌ Login failed"

        except Exception as e:
            message = str(e)

        conn.close()

    return render_template("login.html", message=message)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------- SEARCH (Level 2) ----------------
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []

    if request.method == "POST":
        keyword = request.form["keyword"]

        conn = get_db()
        cursor = conn.cursor()

        # 🚨 vulnerable
        query = f"SELECT username FROM users WHERE username LIKE '%{keyword}%'"
        print(query)

        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except Exception as e:
            results = [("Error: " + str(e),)]

        conn.close()

    return render_template("search.html", results=results)

# ---------------- BLIND SQLi ----------------
@app.route("/blind", methods=["GET", "POST"])
def blind():
    response = ""

    if request.method == "POST":
        payload = request.form["payload"]

        conn = get_db()
        cursor = conn.cursor()

        query = f"SELECT * FROM secrets WHERE secret='{payload}'"
        print(query)

        try:
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                response = "✅ TRUE"
            else:
                response = "❌ FALSE"

        except:
            response = "⚠️ ERROR"

        conn.close()

    return render_template("blind.html", response=response)

if __name__ == "__main__":
    app.run(debug=True)