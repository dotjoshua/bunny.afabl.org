var current_page;
var participant_id = null;
var survey_destination = null;

window.onload = function() {
	bind_handlers();
}

function bind_handlers() {
    jsh.get("#sign_up_button").addEventListener("click", sign_up_handler);
    jsh.get("#agree_button").addEventListener("click", agree_handler);
    jsh.get("#submit_survey_button").addEventListener("click", survey_handler);

    jsh.get("#email_input").addEventListener("keyup", email_input_keyup_handler);
    jsh.get("#work_experience").addEventListener("keyup", decimal_input_keyup_handler);

    jsh.get("#submit_button").addEventListener("click", submit_handler);
}

function submit_handler(e) {
	var file = jsh.get("#submit_input").files[0];

    if (file) {
    	var reader = new FileReader();
		reader.onload = function(e) {
	        var contents = e.target.result;
	        submit_json(contents);
	    };
    	reader.readAsText(file);
    } else { 
    	alert("Failed to load file");
    }
}

function submit_json(json_string) {
	var error_message = null;
	try {
		var parsed_json = JSON.parse(json_string);
	} catch (e) {
		error_message = "This is not a valid json file.";
	}

	if (parsed_json["user_id"] == undefined) {
		error_message = "This json file is not properly structured.";
	}

	if (error_message != null) {
		new jsh.Alert({
			message: error_message,
			title: "Oops!"
		}).open();
		return;
	}

	var req = new XMLHttpRequest();
    req.open("POST", "results/" + parsed_json["user_id"], true);

  	req.setRequestHeader("Content-Type", "application/json");
    req.onreadystatechange = function() {
	    if (req.readyState == 4 && req.status == 200) {
	    	new jsh.Alert({
				message: "We have recieved your results.",
				title: "Thank you!"
			}).open();
			jsh.pages["home"].open();
	    } else {
	    	new jsh.Alert({
				message: "Something went wrong. Please try again.",
				title: "Oops!"
			}).open();
	    }
    };

    req.send(json_string);
}

function sign_up_handler(e) {
	jsh.pages["consent_form"].open();
}

function agree_handler(e) {
	db_action("participants/add", {
		email: jsh.get("#email_input").value
	}, function(response) {
		participant_id = response["participant_id"];
		jsh.pages["survey"].open();
	});
}

function survey_handler(e) {
	var survey_input_ids = [
		"education",
		"major",
		"work_experience",
		"code_experience",
		"game_agent_proficiency",
		"scala_proficiency"
	];

	var survey_complete = true;
	var survey_input_values = {id: participant_id};
	for (var i = 0; i < survey_input_ids.length; i++) {
		var survey_div = jsh.get("#" + survey_input_ids[i]);
		survey_div.classList.remove("empty_input");

		if (survey_div.value == "" 
		|| survey_div.value == "Select" 
		|| (survey_div.getAttribute("regex_pass") == "false")) {
			survey_div.classList.add("empty_input");
			survey_complete = false;
		} else {
			survey_input_values[survey_input_ids[i]] = survey_div.value;
		}
	}

	if (survey_complete) {
		e.target.style.opacity = 0.2;
		e.target.style.pointerEvents = "none"; 
		survey_complete = true;
		db_action("survey_results/add", survey_input_values, function(response) {
			jsh.pages[response["destination"]].open();
			survey_destination = response["destination"];
		});
	}
}

function db_action(url, data, success_callback) {
	new jsh.Request({
		url: url,
		data: data,
		parse_json: true,
		callback: function(response) {
			if (response["success"]) {
				success_callback(response);
			} else {
				new jsh.Alert({
					title: "Oops!", 
					message: jsh.str("An error has occured. ({})", response["error"])
				}).open();
			}
		}
	}).send();
}

function email_input_keyup_handler(e) {
	var re = /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i;
	e.target.setAttribute("regex_pass", validate_input(e.target, re));
}

function decimal_input_keyup_handler(e) {
	var re = /^[0-9]*(\.[0-9][0-9]*){0,1}$/;
	e.target.setAttribute("regex_pass", validate_input(e.target, re));
}

function validate_input(input, re) {
	if (re.test(input.value)) {
		input.style.border = "1px solid #0a0";
		input.style.background = "#fff";
		return true;
	} else {
		input.style.border = "1px solid #a00";
		input.style.background = "rgba(150, 0, 0, 0.2)";
		return false;
	}
}

jsh.addEventListener("page_open", function(e) {
	if (current_page && current_page.name != e.detail.page.name) {
		current_page.div.classList.add("page_slide_out");
		e.detail.page.div.classList.add("page_slide_in");

		setTimeout(function() {	
			for (var page in jsh.pages) {
				jsh.pages[page].div.classList.remove("page_slide_out");
				jsh.pages[page].div.classList.remove("page_slide_in");
			}
		}, 1000);
	}

	current_page = e.detail.page;

	if (e.detail.page.name == "survey" && participant_id == null) {
		jsh.pages["consent_form"].open();
	}

	if (survey_destination && e.detail.page.name != survey_destination) {
		jsh.pages[survey_destination].open();
	}
});