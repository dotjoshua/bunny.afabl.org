from flask import Flask, request, send_from_directory
import re

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

@app.route("/sign_up/", methods=["GET", "POST"])
def sign_up():
    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    email = request.args.get("email")

    if pattern.match(email):
        return "success"
    return "bad email"

if __name__ == "__main__":
    app.run()