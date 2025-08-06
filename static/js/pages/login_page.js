var LoginPage = function() {
	var pub = {};
	var container;
	var emailInput;
	var passwordInput;
	var loginSubmit;

	var constructor = function() {
		container = document.createElement("div");
		container.className = "login-page";

		emailInput = document.createElement("input");
		emailInput.type = "email";
		emailInput.placeholder = "Email";
		emailInput.className = "email-input";
		container.appendChild(emailInput);

		passwordInput = document.createElement("input");
		passwordInput.type = "password";
		passwordInput.placeholder = "Password";
		passwordInput.className = "password-input";
		container.appendChild(passwordInput);

		loginSubmit = document.createElement("button");
		loginSubmit.className = "login-submit";
		loginSubmit.textContent = "LOGIN";
		loginSubmit.onclick = function() {
			login(emailInput.value, passwordInput.value).then(function(data) {
				window.cookieStore.set("token", data.token);
				window.location.search = `?path=/positions`;
			});
		};
		container.appendChild(loginSubmit);
	};

	pub.getContainer = function() {
		return container;
	};

	var login = async function(email, password) {
		const dataToSend = {
			email: email,
			password: password,
		};

		try {
			const response = await fetch(`${API_URL}/user/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(dataToSend)
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const responseData = await response.json();
			return responseData;
		} catch (error) {
			throw error;
		}
	};

	constructor();
	return pub;
};