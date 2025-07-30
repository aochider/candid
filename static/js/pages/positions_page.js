var PositionsPage = function() {
	var pub = {};
	var container;
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

		loading = document.createElement("div");
		loading.className = "loading";
		loading.textContent = "LOADING";
		container.appendChild(loading);

		statement = document.createElement("div");
		statement.className = "statement";
		container.appendChild(statement);

		agree = document.createElement("div");
		agree.className = "agree";
		agree.textContent = "agree";
		agree.onclick = function() {
			respond('agree');
		};
		container.appendChild(agree);


		disagree = document.createElement("div");
		disagree.className = "disagree";
		disagree.textContent = "disagree";
		disagree.onclick = function() {
			respond('disagree');
		};
		container.appendChild(disagree);

		pass = document.createElement("div");
		pass.className = "pass";
		pass.textContent = "pass";
		pass.onclick = function() {
			respond('pass');
		};
		container.appendChild(pass);

		chat = document.createElement("div");
		chat.className = "chat";
		chat.textContent = "chat";
		chat.onclick = function() {
			respond('chat').then(function(data) {
				doChat().then(function(data2) {
					window.location.search = "?path=/chat&chat_log_id=" + data2.id;
				});
			});
		};
		container.appendChild(chat);

		let positions = getPositions();
		positions.then(function(data) {
			console.log(data);
			positionsQueue = data.positions;
			pub.nextPosition();
		})
		.catch(function(err) {
			console.log(err);
		})
		.finally(function() {
			console.log('finally');
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

	var getPositions = async function() {
		try {
			const response = await fetch(`${API_URL}/position/queue`, {
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

	var respond = async function(result) {
		const dataToSend = {
			result: result,
		};

		try {
			const response = await fetch(`${API_URL}/user_position/position/${currentPosition.id}/respond`, {
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

	var doChat = async function() {
		const dataToSend = {
		};

		try {
			console.log('test');
			const response = await fetch(`${API_URL}/chat_log/position/${currentPosition.id}`, {
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