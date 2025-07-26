var ChatPage = function() {
	var pub = {};

	var constructor = function() {
		var cont = document.createElement("div");
		cont.className = "chat-page";
		pub.container = cont;
	};

	pub.getContainer = function() {
		return pub.container;
	};

	constructor();
	return pub;
};