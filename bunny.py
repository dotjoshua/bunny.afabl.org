from flask import Flask, request, send_from_directory, Response
import re
import sqlite3
import random
import json
import zipfile
import os
import io
import time

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


@app.route('/results/<path:participant_id>', methods=['GET', 'POST'])
def save_results(participant_id):
    response = {}
    response["success"] = True
    response_code = 200

    participant_id = re.sub("([^0-9])", "", participant_id)[0:8]

    data = request.data
    json_data = json.loads(data.decode("utf-8"))
    if len(participant_id) == 0 or int(json_data["user_id"]) != int(participant_id):
        response["success"] = False
        response["error"] = "Invalid participant ID"
        response_code = 400

    filename = "results/submissions/{}/{}{}.json".format(participant_id, str(time.time()), str(random.random()))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as json_file:
        json_file.write(data)
    
    return json.dumps(response), response_code


@app.route("/afabl_resources/", methods=["POST", "GET"])
def get_afabl_resources():
    participant_id = re.sub("([^0-9])", "", request.values["id"])[0:8]

    zip_bytes = io.BytesIO()
    zip_obj = zipfile.ZipFile(zip_bytes, "w")

    afabl_path = "afabl_resources"
    for root, dirs, files in os.walk(afabl_path):
        for f in files:
            file_path = os.path.join(root, f)
            with open(file_path) as file_contents:
                zip_obj.writestr(file_path, file_contents.read().replace("<--PARTICIPANT_ID--/>", str(participant_id)))

    zip_obj.close()

    results = zip_bytes.getvalue()
    return Response(results, mimetype="text/plain", headers={"Content-Disposition": "attachment;filename=afabl_resources.zip"})


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
