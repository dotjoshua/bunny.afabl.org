CREATE TABLE participants (
	id varchar(8) NOT NULL, 
	email VARCHAR(255), 
	scala BOOLEAN,
	afabl BOOLEAN,
	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id)
);

CREATE TABLE survey_results (
	id VARCHAR(8) NOT NULL, 
	education INTEGER NOT NULL,
	major INTEGER NOT NULL,
	work_experience decimal NOT NULL, 
	code_experience INTEGER NOT NULL,
	game_agent_proficiency INTEGER NOT NULL,
	scala_proficiency INTEGER NOT NULL,
	FOREIGN KEY (id) REFERENCES participants(id),
	FOREIGN KEY (education) REFERENCES educations(id),
	FOREIGN KEY (major) REFERENCES majors(id),
	FOREIGN KEY (code_experience) REFERENCES code_experiences(id),
	FOREIGN KEY (game_agent_proficiency) REFERENCES game_agent_proficiencies(id),
	FOREIGN KEY (scala_proficiency) REFERENCES scala_proficiencies(id),
	PRIMARY KEY (id)
);

CREATE TABLE educations (
	id INTEGER NOT NULL,
	education VARCHAR(255),
	PRIMARY KEY (id)
);

CREATE TABLE majors (
	id INTEGER NOT NULL,
	major VARCHAR(255),
	PRIMARY KEY (id)
);

CREATE TABLE code_experiences (
	id INTEGER NOT NULL,
	code_experience VARCHAR(255),
	PRIMARY KEY (id)
);

CREATE TABLE game_agent_proficiencies (
	id INTEGER NOT NULL,
	game_agent_proficiency VARCHAR(255),
	PRIMARY KEY (id)
);

CREATE TABLE scala_proficiencies (
	id INTEGER NOT NULL,
	scala_proficiency VARCHAR(255),
	PRIMARY KEY (id)
);

INSERT INTO educations (id, education) VALUES (0, "High School");
INSERT INTO educations (id, education) VALUES (1, "Associate Degree or currently enrolled in Bachelor degree program");
INSERT INTO educations (id, education) VALUES (2, "Bachelor Degree");
INSERT INTO educations (id, education) VALUES (3, "Master Degree");
INSERT INTO educations (id, education) VALUES (4, "Doctoral Degree");

INSERT INTO majors (id, major) VALUES (0, "Computer Science");
INSERT INTO majors (id, major) VALUES (1, "Computer Engineering");
INSERT INTO majors (id, major) VALUES (2, "Electrical Engineering");
INSERT INTO majors (id, major) VALUES (3, "Other Technical (STEM)");
INSERT INTO majors (id, major) VALUES (4, "Other Non-Technical");

INSERT INTO code_experiences (id, code_experience) VALUES (0, "~100 lines of code");
INSERT INTO code_experiences (id, code_experience) VALUES (1, "~1000 lines of code");
INSERT INTO code_experiences (id, code_experience) VALUES (2, "~10,000 lines of code");
INSERT INTO code_experiences (id, code_experience) VALUES (3, "50,000+ lines of code");

INSERT INTO game_agent_proficiencies (id, game_agent_proficiency) VALUES (0, "Not proficient");
INSERT INTO game_agent_proficiencies (id, game_agent_proficiency) VALUES (1, "Familiar (have done tutorials or simple examples)");
INSERT INTO game_agent_proficiencies (id, game_agent_proficiency) VALUES (2, "Proficient (can write programs with multiple objects and files)");
INSERT INTO game_agent_proficiencies (id, game_agent_proficiency) VALUES (3, "Expert");

INSERT INTO scala_proficiencies (id, scala_proficiency) VALUES (0, "Not proficient");
INSERT INTO scala_proficiencies (id, scala_proficiency) VALUES (1, "Familiar (have done tutorials or simple examples)");
INSERT INTO scala_proficiencies (id, scala_proficiency) VALUES (2, "Proficient (can write programs with multiple objects and files)");
INSERT INTO scala_proficiencies (id, scala_proficiency) VALUES (3, "Expert");