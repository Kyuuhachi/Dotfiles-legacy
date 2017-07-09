(function() {
	buffer.incrementURL = function incrementURL(count) {
		let { dactyl } = this.modules;
		let path = this.uri.path;

		let start = -1, end = -1;
		for(var i = 1; i < path.length; i++)
			if(path[i] == '%')
			i += 2;
		else if(path[i].match(/\d/)) {
			start = i;
			while(i < path.length && path[i].match(/\d/)) i++;
			end = i;
		}
		if(start >= 0) {
			let pre = path.substring(0, start);
			let num = path.substring(start, end);
			let post = path.substring(end);
			let newNum = String(Math.max(parseInt(num, 10) + count, 0));
			if(num.match(/^0/))
				while(newNum.length < num.length)
				newNum = "0" + newNum;
			dactyl.open(this.uri.prePath + pre + newNum + post);
		}
	};

	let $ = document.querySelector.bind(document); // Really primitive implementation of jQuery
	$("#dactyl-addon-bar").append($("#PanelUI-button"));
})();
