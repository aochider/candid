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
		pub.container = container;

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
				console.log('TODO nav to chat');
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
		return pub.container;
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
		/*
		const dataToSend = {
			name: 'John Doe',
			email: 'john.doe@example.com'
		};*/

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
			const response = await fetch(`${API_URL}/position/${currentPosition.id}/respond`, {
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