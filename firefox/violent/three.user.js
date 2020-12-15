// ==UserScript==
// @name     Three.js docs
// @version  1
// @include  https://threejs.org/docs/*
// @grant    none
// @require  https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js
// @require  https://threejs.org/docs/prettify/prettify.js
// @require  https://threejs.org/docs/list.js
// @run-at   document-end
// ==/UserScript==

// Requires adblocking «https://threejs.org/docs/page.js»

/* global list, $ */

console.log(list)

let path, localizedPath;
let pathname = window.location.pathname;
let section = /\/(manual|api|examples)\//.exec(pathname)[1].toString().split(".html")[0];
let name = /[-A-z0-9]+\.html/.exec(pathname).toString().split(".html")[0];

switch(section) {
	case "api":
		localizedPath = /\/api\/[A-z0-9/]+/.exec(pathname).toString().substr(5);
		path = localizedPath.replace(/^[A-z0-9-]+\//, "");
		break;

	case "examples":
		path = localizedPath = /\/examples\/[A-z0-9/]+/.exec(pathname).toString().substr(10);
		break;

	case "manual":
		name = name.replace(/-/g, " ");
		path = pathname.replace(/ /g, "-");
		path = localizedPath = /\/manual\/[-A-z0-9/]+/.exec(path).toString().substr(8);
		break;
}

var text = document.body.innerHTML;

function urlfor(page) {
	return page
}

const BUILTINS_S = "null this Boolean Object Array Number String Integer Float TypedArray ArrayBuffer";
const BUILTINS = new Set([...BUILTINS_S.split(" "), ...BUILTINS_S.toLowerCase().split(" ")]);

function parse(s) {
	return s.replace(/\[(\w+):(?! )([^\]]+)(?<! )]((?:\s*\(.*\))?)/gi, (text, cmd, arg, params) => {
		function param(type) {
			if(BUILTINS.has(type))
				return $("<span class=param>").text(type);
			else
				return $("<a class=param>").text(type).attr("href", urlfor(type));
		}

		function split(s) {
			const [_, a, b] = /^(\S+)(?: (.+))?$/.exec(s);
			return [a, b || a];
		}

		if(arg === undefined) {
			if(cmd == "name") return name;
			if(cmd == "path") return path;
		} else {
			if(cmd == "page") {
				let [what, label] = split(arg);
				return $("<span>")
					.append($("<a>")
						.text(label)
						.attr("href", urlfor(arg.startsWith(".") ? name + what : what))
					).attr("title", text)[0].outerHTML + params
			}

			if(cmd == "param") {
				let [type, what] = split(arg);
				return $("<span>")
					.append(what)
					.append(" : ")
					.append(param(type))
					.attr("title", text)[0].outerHTML + params
			}

			if(cmd == "member" || cmd == "property") {
				let [type, what] = split(arg);
				return $("<span>")
					.append(".")
					.append($("<a>")
						.text(what)
						.attr("href", name + "." + what))
					.append(" : ")
					.append(param(type))
					.attr("title", text)[0].outerHTML + params + params
			}

			if(cmd == "method") {
				let [type, what] = split(arg);
				return $("<span>")
					.append(".")
					.append($("<a>")
						.text(what)
						.attr("href", name + "." + what))
					.append(" ")
					.append(parse(params))
					.append(" : ")
					.append(param(type))
					.attr("title", text)[0].outerHTML
			}

			if(cmd == "link") {
				let [url, label] = split(arg);
				return $("<span>")
					.append($("<a>")
						.text(label)
						.attr("href", url))
					.attr("title", text)[0].outerHTML + params
			}
		}
		return text;
	});
}

text = text.replace(/\[name\]/gi, name);
text = text.replace(/\[path\]/gi, path);

text = parse(text);
text = text.replace(/\*([\w\d"\-(][\w\d \-+\-()=,."]*[\w\d")]|\w)\*/gi, "<strong>$1</strong>"); // *

// text = text.replace(/\[page:([\w.]+)\]/gi, "[page:$1 $1]"); // [page:name] to [page:name title]
// text = text.replace(/\[page:\.([\w.]+) ([\w.\s]+)\]/gi, "[page:" + name + ".$1 $2]"); // [page:.member title] to [page:name.member title]
// text = text.replace(/\[page:([\w.]+) ([\w.\s]+)\]/gi, "<a href=\"window.parent.setUrlFragment('$1')\" title=\"$1\">$2</a>"); // [page:name title]
// // text = text.replace( /\[member:.([\w]+) ([\w\.\s]+)\]/gi, "<a href=\"window.parent.setUrlFragment('" + name + ".$1')\" title=\"$1\">$2</a>" );

// text = text.replace(/\[(member|property|method|param):([\w]+)\]/gi, "[$1:$2 $2]"); // [member:name] to [member:name title]
// text = text.replace(/\[(?:member|property|method):([\w]+) ([\w.\s]+)\]\s*(\(.*\))?/gi, `<a href="window.parent.setUrlFragment('${name}.$2')" title="${name}.$2" class="permalink">#</a> .<a href="window.parent.setUrlFragment('" + name + ".$2')" id="$2">$2</a> $3 : <a class="param" href="window.parent.setUrlFragment('$1')">$1</a>`);
// text = text.replace(/\[param:([\w.]+) ([\w.\s]+)\]/gi, "$2 : <a class=\"param\" href=\"window.parent.setUrlFragment('$1')\">$1</a>"); // [param:name title]

// text = text.replace(/\[link:([\w:/.\-_]+)\]/gi, "[link:$1 $1]"); // [link:url] to [link:url title]
// text = text.replace(/\[link:([\w:/.\-_()?#=!]+) ([\w:/.\-_\s]+)\]/gi, "<a href=\"$1\"  target=\"_blank\">$2</a>"); // [link:url title]


// text = text.replace(/\[example:([\w_]+)\]/gi, "[example:$1 $1]"); // [example:name] to [example:name title]
// text = text.replace(/\[example:([\w_]+) ([\w:/.\-_ \s]+)\]/gi, "<a href=\"../examples/#$1\"  target=\"_blank\">$2</a>"); // [example:name title]

// text = text.replace(/<a class="param" href="window.parent.setUrlFragment\('\w+'\)">(null|this|Boolean|Object|Array|Number|String|Integer|Float|TypedArray|ArrayBuffer)<\/a>/gi, '<span class="param">$1</span>'); // remove links to primitive types

document.body.innerHTML = text;

console.log(document);
$("code")
	.addClass("prettyprint")
	.attr("translate", "no")
	.each((_, e) => e.textContent = e.textContent.trim().replace(/^\t\t/gm, ""));

$('<a id="button"><img src="../files/ic_mode_edit_black_24dp.svg"></a>')
	.attr("href", `https://github.com/mrdoob/three.js/blob/dev/docs/${section}/${localizedPath}.html`)
	.appendTo(document.body);

const prefix = pathname.substring(0, pathname.indexOf("docs") + 4);

$("<link rel=stylesheet>").attr("href", prefix + "/prettify/prettify.css").appendTo(document.head);
$("<link rel=stylesheet>").attr("href", prefix + "/prettify/threejs.css").appendTo(document.head);
prettyPrint();
