import csv
import sqlite3

conn = sqlite3.connect("bunny.sqlt")
c = conn.cursor()

c.execute("SELECT * FROM survey_results")
survey_results_data = c.fetchall()

survey_results = []
for survey_result_data in survey_results_data:
	participant_id = survey_result_data[0]

	c.execute("SELECT * FROM participants WHERE id=?", [participant_id])
	participant_data = c.fetchone()

	survey_result = {}
	survey_result["ID"] = participant_id
	survey_result["Email"] = participant_data[1]
	survey_result["AFABL"] = participant_data[2] == 1
	survey_result["Scala"] = participant_data[3] == 1

	education_ans = survey_result_data[1]
	major_ans = survey_result_data[2]
	work_experience_ans = survey_result_data[3]
	code_experience_ans = survey_result_data[4]
	game_agent_proficiency_ans = survey_result_data[5]
	scala_proficiency_ans = survey_result_data[6]

	c.execute("SELECT education FROM educations WHERE id=?", [education_ans])
	survey_result["Education"] = c.fetchone()[0]

	c.execute("SELECT major FROM majors WHERE id=?", [major_ans])
	survey_result["Major"] = c.fetchone()[0]

	survey_result["Work Experience"] = work_experience_ans

	c.execute("SELECT code_experience FROM code_experiences WHERE id=?", [code_experience_ans])
	survey_result["Code Experience"] = c.fetchone()[0]

	c.execute("SELECT game_agent_proficiency FROM game_agent_proficiencies WHERE id=?", [game_agent_proficiency_ans])
	survey_result["Game Agent Proficiency"] = c.fetchone()[0]

	c.execute("SELECT scala_proficiency FROM scala_proficiencies WHERE id=?", [scala_proficiency_ans])
	survey_result["Scala Proficiency"] = c.fetchone()[0]

	survey_results.append(survey_result)

conn.close()

if len(survey_results) > 0:
	with open('../results/participant_data.csv', 'w') as f:
		w = csv.DictWriter(f, sorted(list(survey_results[0].keys())))
		w.writeheader()
		for survey_result in survey_results:
			w.writerow(survey_result)