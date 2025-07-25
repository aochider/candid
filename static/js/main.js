var main = function() {
	var API_URL = "http://localhost:8000";
	const xhr = new XMLHttpRequest();

	// 2. Configure the request: specify the HTTP method (GET), and the URL
	xhr.open('GET', `${API_URL}/user`, true); // 'true' for asynchronous request

	// 3. Set up a function to handle the response when the request is complete
	xhr.onload = function() {
		// Check if the request was successful (HTTP status 200)
		if (xhr.status === 200) {
			// Parse the JSON response
			const data = JSON.parse(xhr.responseText);
			console.log('Data received:', data);
			// You can now use 'data' to update your web page or perform other actions
		} else {
			// Handle errors
			console.error('Request failed. Status:', xhr.status, 'Status Text:', xhr.statusText);
		}
	};

	// 4. Set up a function to handle network errors
	xhr.onerror = function() {
		console.error('Network error occurred.');
	};

	// 5. Send the request
	xhr.send();
};

window.addEventListener("DOMContentLoaded", main);