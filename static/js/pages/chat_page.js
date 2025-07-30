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
				console.log(data);
			});
		};
		container.appendChild(messageSubmit);

		getMessages().then(function(data) {
			var messages = data.messages;
			messageBox.textContent += JSON.stringify(messages);
			if (messages[messages.length - 1]) {
				lastMessageId = messages[messages.length - 1].id;
			}
			startPollMessages();
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
			messageBox.textContent += JSON.stringify(messages);
			if (messages[messages.length - 1]) {
				lastMessageId = messages[messages.length - 1].id;
			}
			startPollMessages();
		});
	};

	constructor();
	return pub;
};