var Header = function() {
	var pub = {};
	var container;

	var constructor = function() {
		container = document.createElement("div");
		container.className = "header";
		container.textContent = "header";
	};

	pub.getContainer = function() {
		return container;
	};

	constructor();
	return pub;
};