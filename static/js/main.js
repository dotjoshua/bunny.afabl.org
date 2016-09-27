window.onload = function() {
    jsh.pages["sign_up"].open();

    jsh.get("#sign_up_input").addEventListener("keypress", function(e) {
    	validate_email_field(e.target);

    	if (e.keyCode == 13) {
    		sign_up(e.target);
    	}
    });

    jsh.get("#sign_up_button").addEventListener("click", function(e) {
    	sign_up(jsh.get("#sign_up_input"));
    });
}

function sign_up(input) {
	if (validate_email_field(input)) {
		new jsh.Request({
			url: "sign_up",
			data: {
				"email": input.value
			}, 
			callback: function(result) {
				new jsh.Alert({
					title: "Thanks!", 
					message: "We'll let you know when the study is ready."
				}).open();
				input.value = "";
			}
		}).send();
	} else {
		new jsh.Alert({
			title: "Oops!",
			message: "Please enter a valid email address"
		}).open();
	}
}

function validate_email_field(input) {
	var re = /^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i;
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