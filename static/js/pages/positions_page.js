var PositionsPage = function() {
	var pub = {};
	var container;
	var header;
	var card;
	var loading;
	var statement;
	var agree;
	var disagree;
	var pass;
	var chat;
	var positionsQueue = [];
	var currentPosition;

	var constructor = function() {
		container = document.createElement("div");
		container.className = "positions-page";

		header = Header();
		container.appendChild(header.getContainer());

		card = document.createElement("div");
		card.className = "card";
		container.appendChild(card);

		loading = document.createElement("div");
		loading.className = "loading";
		loading.textContent = "LOADING";
		card.appendChild(loading);

		statement = document.createElement("div");
		statement.className = "statement";
		card.appendChild(statement);

		agree = document.createElement("div");
		agree.className = "respond agree";
		agree.textContent = "agree";
		agree.onclick = function() {
			respond('agree');
		};
		card.appendChild(agree);

		disagree = document.createElement("div");
		disagree.className = "respond disagree";
		disagree.textContent = "disagree";
		disagree.onclick = function() {
			respond('disagree');
		};
		card.appendChild(disagree);

		pass = document.createElement("div");
		pass.className = "respond pass";
		pass.textContent = "pass";
		pass.onclick = function() {
			respond('pass');
		};
		card.appendChild(pass);

		chat = document.createElement("div");
		chat.className = "respond chat";
		chat.textContent = "chat";
		chat.onclick = function() {
			respond('chat').then(function(data) {
				apiRequest(`/chat_log/position/${currentPosition.id}`, "POST", {}).then(function(data2) {
					window.location.search = `?path=/chat&chat_log_id=${data2.id}`;
				})
				.catch(function(err) {
					console.log(err);
					window.location.search = `?path=/login&error=${err}`;
				});
			})
			.catch(function(err) {
				console.log(err);
				window.location.search = `?path=/login&error=${err}`;
			});
		};
		card.appendChild(chat);

		apiRequest("/position/queue", "GET").then(function(data) {
			positionsQueue = data.positions;
			pub.nextPosition();
		})
		.catch(function(err) {
			console.log(err);
			window.location.search = `?path=/login&error=${err}`;
		})
		.finally(function() {
			pub.hideLoading();
		});
	};

	pub.getContainer = function() {
		return container;
	};

	pub.hideLoading = function() {
		loading.style.display = "none";
	};

	pub.showLoading = function() {
		loading.style.display = "";
	};

	pub.nextPosition = function() {
		currentPosition = positionsQueue.shift();
		if (!currentPosition) {
			statement.textContent = "No more positions left!";
		} else {
			statement.textContent = currentPosition.statement;
		}
	};

	var respond = async function(result) {
		return apiRequest(`/user_position/position/${currentPosition.id}`, "POST", { result });
	};

	constructor();
	return pub;
};