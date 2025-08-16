var LoginPage = function() {
	var pub = {};
	var container;
	var card;
	var logo;
	var form;
	var emailInput;
	var passwordInput;
	var loginSubmit;

	var constructor = function() {
		const urlParams = new URLSearchParams(window.location.search);
		errorText = urlParams.get("error");

		container = document.createElement("div");
		container.className = "login-page";

		card = document.createElement("div");
		card.className = "card";
		container.appendChild(card);

		logo = document.createElement("div");
		logo.className = "logo";
		logo.textContent = "Candid";
		card.appendChild(logo);

		error = document.createElement("div");
		error.className = "error";
		error.textContent = errorText;
		if (errorText) {
			card.appendChild(error);
		}

		form = document.createElement("form");
		form.className = "form";
		form.method = "POST";
		form.onsubmit = function() {
			apiRequest("/user/login", "POST", {"email": emailInput.value, "password": passwordInput.value}).then(function(data) {
				window.cookieStore.set("user_id", data.id);
				window.cookieStore.set("token", data.token);
				window.location.search = `?path=/positions`;
			})
			.catch(function(err) {
				console.log(err);
				window.location.search = `?path=/login&error=${err}`;
			});

			return false;
		};
		card.appendChild(form);

		emailInput = document.createElement("input");
		emailInput.type = "email";
		emailInput.placeholder = "Email";
		emailInput.className = "email-input";
		emailInput.name = "email";
		form.appendChild(emailInput);

		passwordInput = document.createElement("input");
		passwordInput.type = "password";
		passwordInput.placeholder = "Password";
		passwordInput.className = "password-input";
		passwordInput.name = "password";
		form.appendChild(passwordInput);

		loginSubmit = document.createElement("input");
		loginSubmit.type = "submit";
		loginSubmit.className = "login-submit";
		loginSubmit.value = "LOGIN";
		form.appendChild(loginSubmit);
	};

	pub.getContainer = function() {
		return container;
	};

	constructor();
	return pub;
};