from flask import Flask, request, send_from_directory
import re
import sqlite3
import random
import json

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

@app.route("/survey_results/add/", methods=["POST", "GET"])
def add_survey_result():
    response = {}
    response["success"] = True

    conn = sqlite3.connect("db/bunny.sqlt")
    c = conn.cursor()

    participant_id = request.values["id"]
    survey_inputs = ["education", "major", "work_experience", "code_experience", "game_agent_proficiency", "scala_proficiency"];
    survey_results = [participant_id]
    for survey_inputs in survey_inputs:
        survey_results.append(request.values[survey_inputs])

    if random.random() > 0.5:
        response["destination"] = "afabl"
    else:
        response["destination"] = "scala"

    try:
        c.execute("UPDATE participants SET {} = 1 WHERE id=?".format(response["destination"]), [participant_id])
        c.execute("INSERT INTO survey_results (id, education, major, work_experience, code_experience, game_agent_proficiency, scala_proficiency) VALUES (?, ?, ?, ?, ?, ?, ?)", survey_results)
    except Exception as e:
        response["success"] = False
        response["error"] = str(e)

    conn.commit()
    conn.close()
    return json.dumps(response)


@app.route("/participants/add/", methods=["POST", "GET"])
def add_participant():
    response = {}
    response["success"] = True

    pattern = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    email = request.values["email"]
    if not pattern.match(email) and len(email) > 0:
        response["success"] = False
        response["error"] = "bad email address"
        return json.dumps(response)

    if email == "":
        email = None

    conn = sqlite3.connect("db/bunny.sqlt")
    c = conn.cursor()

    try:
        id_exists = 0
        participant_id = "0" * 8
        while id_exists == 0:
            participant_id = (("0" * 8) + str(int(random.random() * 100000000)))[-8:]
            c.execute("SELECT EXISTS(SELECT 1 FROM participants WHERE id=? LIMIT 1);", [participant_id])
            id_exists = c.fetchone()

        c.execute("INSERT INTO participants (id, email) VALUES (?, ?)", [participant_id, email])
        response["participant_id"] = participant_id
    except Exception as e:
        response["success"] = False
        response["error"] = str(e)

    conn.commit()
    conn.close()
    return json.dumps(response)

if __name__ == "__main__":
    app.run()