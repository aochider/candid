var ChatPage = function() {
	var pub = {};
	var chatLogId;
	var lastMessageId = 0;
	var container;
	var messageBox;
	var messageInput;
	var messageSubmit;

	var constructor = function() {
		const urlParams = new URLSearchParams(window.location.search);
		chatLogId = urlParams.get("chat_log_id");

		container = document.createElement("div");
		container.className = "chat-page";

		messageBox = document.createElement("div");
		messageBox.className = "message-box";
		container.appendChild(messageBox);

		messageInput = document.createElement("textarea");
		messageInput.className = "message-input";
		container.appendChild(messageInput);

		messageSubmit = document.createElement("button");
		messageSubmit.className = "message-submit";
		messageSubmit.textContent = "SEND";
		messageSubmit.onclick = function() {
			sendMessage(messageInput.value).then(function(data) {
				console.log("sent!", data);
			})
			.catch(function(err) {
				console.log(err);
				window.location.search = `?path=/login`;
			});
		};
		container.appendChild(messageSubmit);

		getMessages().then(function(data) {
			var messages = data.messages;
			messageBox.textContent += messages.length ? JSON.stringify(messages) : "";
			lastMessageId = messages[messages.length - 1]?.id ?? lastMessageId;
			startPollMessages();
		})
		.catch(function(err) {
			console.log(err);
			window.location.search = `?path=/login`;
		});
	};

	pub.getContainer = function() {
		return container;
	};

	var getMessages = async function() {
		try {
			const response = await fetch(`${API_URL}/chat_log_message/chat_log/${chatLogId}`, {
				method: 'GET',
				headers: {
					'Authorization': `Bearer ${(await window.cookieStore.get("token")).value}`,
					'Content-Type': 'application/json'
				},
				body: undefined, //JSON.stringify(dataToSend)
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

	var sendMessage = async function(message) {
		const dataToSend = {
			message: message,
		};

		try {
			const response = await fetch(`${API_URL}/chat_log_message/chat_log/${chatLogId}`, {
				method: 'POST',
				headers: {
					'Authorization': `Bearer ${(await window.cookieStore.get("token")).value}`,
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

	var pollMessages = async function() {
		try {
			const response = await fetch(`${API_URL}/chat_log_message/chat_log/${chatLogId}/message_offset/${lastMessageId}`, {
				method: 'GET',
				headers: {
					'Authorization': `Bearer ${(await window.cookieStore.get("token")).value}`,
					'Content-Type': 'application/json'
				},
				body: undefined, //JSON.stringify(dataToSend)
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

	var startPollMessages = function() {
		pollMessages().then(function(data) {
			var messages = data.messages;
			messageBox.textContent += messages.length ? JSON.stringify(messages) : "";
			lastMessageId = messages[messages.length - 1]?.id ?? lastMessageId;
			startPollMessages();
		})
		.catch(function(err) {
			console.log(err);
			window.location.search = `?path=/login`;
		});
	};

	constructor();
	return pub;
};