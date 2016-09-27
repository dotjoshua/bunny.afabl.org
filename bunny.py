from flask import Flask, request, send_from_directory
import re
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    with open("index.html") as index_file:
        result = index_file.read()
    return result

@app.route("/css/<path:path>")
def serve_css(path):
    return send_from_directory("static/css", path)

@app.route("/lib/<path:path>")
def serve_lib(path):
    return send_from_directory("static/lib", path)

@app.route("/js/<path:path>")
def serve_js(path):
    return send_from_directory("static/js", path)

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    email = request.args.get("email")

    result = "Error: bad email", 400

    if pattern.match(email):
        conn = sqlite3.connect("db/bunny.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO sign_up (email) VALUES (?)", [email])
        except sqlite3.IntegrityError:
            pass
        result = "success"
        conn.commit()
        conn.close()

    return result

if __name__ == "__main__":
    app.run()