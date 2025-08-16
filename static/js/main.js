const API_URL = "http://localhost:8000";

var main = function() {
    const urlParams = new URLSearchParams(window.location.search);
	var path = urlParams.get("path");
	var body = document.getElementsByTagName("body")[0];

	switch (path) {
		case '/positions':
			var page = PositionsPage();
			body.appendChild(page.getContainer());
			break;
		case '/chat':
			var page = ChatPage();
			body.appendChild(page.getContainer());
			break;
		case '/login':
			var page = LoginPage();
			body.appendChild(page.getContainer());
			break;
	}
};

window.addEventListener("DOMContentLoaded", main);

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(';').shift();
}

async function apiRequest(path, method, body) {
	const response = await fetch(`${API_URL}${path}`, {
		method: method,
		headers: {
			'Authorization': `Bearer ${getCookie("token")}`,
			'Content-Type': 'application/json'
		},
		body: body ? JSON.stringify(body) : undefined,
	});

	if (!response.ok) {
		throw new Error(await response.text());
	}

	return await response.json();
}