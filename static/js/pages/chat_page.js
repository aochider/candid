var ChatPage = function() {
	var pub = {};
	var chatLogId;
	var userId;
	var lastMessageId = 0;
	var container;
	var header;
	var card;
	var messageBox;
	var inputBox;
	var form;
	var messageInput;
	var messageSubmit;

	var constructor = function() {
		const urlParams = new URLSearchParams(window.location.search);
		chatLogId = urlParams.get("chat_log_id");
		userId = parseInt(getCookie("user_id"), 10);

		container = document.createElement("div");
		container.className = "chat-page";

		header = Header();
		container.appendChild(header.getContainer());

		card = document.createElement("div");
		card.className = "card";
		container.appendChild(card);

		messageBox = document.createElement("div");
		messageBox.className = "message-box";
		container.appendChild(messageBox);

		inputBox = document.createElement("div");
		inputBox.className = "input-box";
		container.appendChild(inputBox);

		form = document.createElement("form");
		form.action = "POST";
		form.onsubmit = function() {
			apiRequest(`/chat_log_message/chat_log/${chatLogId}`, "POST", {"message": messageInput.value}).then(function(data) {
				console.log("sent!", data);
				messageInput.value = "";
			})
			.catch(function(err) {
				console.log(err);
				window.location.search = `?path=/login&error=${err}`;
			});

			return false;
		};
		inputBox.appendChild(form);

		messageInput = document.createElement("input");
		messageInput.className = "message-input";
		messageInput.name = "message";
		messageInput.placeholder = "Type a message here...";
		messageInput.type = "text";
		form.appendChild(messageInput);

		messageSubmit = document.createElement("input");
		messageSubmit.type = "submit";
		messageSubmit.className = "message-submit";
		messageSubmit.value = "❯";
		form.appendChild(messageSubmit);

		apiRequest(`/chat_log/${chatLogId}`, "GET").then(function(data) {
			card.textContent = data.statement;
		})
		.catch(function(err) {
			console.log(err);
			window.location.search = `?path=/login&error=${err}`;
		});
		apiRequest(`/chat_log_message/chat_log/${chatLogId}`, "GET").then(function(data) {
			renderMessages(data.messages);
			startPollMessages();
		})
		.catch(function(err) {
			console.log(err);
			window.location.search = `?path=/login&error=${err}`;
		});
	};

	pub.getContainer = function() {
		return container;
	};

	var pollMessages = async function() {
		return apiRequest(`/chat_log_message/chat_log/${chatLogId}/chat_log_message_id_offset/${lastMessageId}`, "GET");
	};

	var startPollMessages = function() {
		pollMessages().then(function(data) {
			renderMessages(data.messages);
			startPollMessages();
		})
		.catch(function(err) {
			console.log(err);
			window.location.search = `?path=/login&error=${err}`;
		});
	};

	var renderMessages = function(messages) {
		for (var i = 0; i < messages.length; i++) {
			var message = messages[i];
			var bubble = SelfChatBubble();
			if (message.user_id !== userId) {
				bubble = OtherChatBubble();
			}
			bubble.setMessage(message.message);
			messageBox.appendChild(bubble.getContainer());
			lastMessageId = message.id;
			window.scrollTo(0, document.body.scrollHeight);
		}
	};

	constructor();
	return pub;
};