var PositionsPage = function() {
	var pub = {};
	var container;
	var loading;
	var statement;
	var positionsQueue = [];

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
		var nextPosition = positionsQueue.shift();
		if (!nextPosition) {
			statement.textContent = "No more positions left!";
		} else {
			statement.textContent = nextPosition.statement;
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

	constructor();
	return pub;
};