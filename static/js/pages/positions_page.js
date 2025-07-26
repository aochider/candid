var PositionsPage = function() {
	var pub = {};

	var constructor = function() {
		var cont = document.createElement("div");
		cont.className = "positions-page";
		pub.container = cont;
	};

	pub.getContainer = function() {
		return pub.container;
	};

	constructor();
	return pub;
};