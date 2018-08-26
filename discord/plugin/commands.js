/* global Modules, MonkeyPatch, Renderer, ReactComponents */
"use strict";
(async function() {
	const Chat = await Modules.byFields("sendBotMessage");
	const MessageList = await Modules.byFields("getLastEditableMessage");
	const MessageTools = await Modules.byFields("editMessage", "deleteMessage");
	const NicknameTools = await Modules.find(a => Object.keys(a).length == 1 && a.changeNickname);
	const Emojis = await Modules.byFields("getDisambiguatedEmojiContext");
	const HTTP = await Modules.byFields("get", "post", "put", "patch", "delete");
	const User = await Modules.byFields("getCurrentUser");

	Modules.byCode("\"Channel\"").then(alert)
	let m = Modules.require(6191)
	console.log(m)
	for(let a in m) {
		console.log(a,m[a])
	}

	alert("asdf")
	ReactComponents.get("Channel").then(_ => console.log(_));
	const CTAF = ReactComponents.get("ChannelTextAreaForm");
	alert("asdf")
	MonkeyPatch(CTAF, "handleSendMessage", { instead: ({call, args: [text], args, that:{props:{channel}}}) => {
		if(text.startswith("::")) {
			args[0] = args[0].slice(1);
			return call();
		}
		if(text[0] === ":") {
			console.log(text, channel, call());
		}
		return call();
	} });
	Renderer.rebindMethods(CTAF, "handleSendMessage");
	alert("asdf")

	function parseCommand(s) {
		let count = "";
		if(/[1-9]/.test(s[0])) do {
			count += s[0];
			s = s.slice(1);
		} while(/[0-9]/.test(s[0]));

		let sep = /(?=[\x00-\x7F])[^a-zA-Z0-9\\]/;

		let out = [];
		let part = "";
		while(s) {
			if(s[0].match(sep)) {
				sep = s[0];
				out.push(part);
				part = "";
				s = s.slice(1);
				break;
			} else part += s[0];
			s = s.slice(1);
		}
		while(s) {
			if(s[0] === "\\") {
				if(s[1] === sep)
					part += s[1];
				else
					part += s[0] + (s[1]||"");
				s = s.slice(1);
			} else if(s[0] === sep) {
				sep = s[0];
				out.push(part);
				part = "";
			} else part += s[0];
			s = s.slice(1);
		}
		out.push(part);
		return [count ? parseInt(count, 10) : undefined, out];
	}

	function handleMessage(channel, s) {
		const user = User.getCurrentUser();
		try {
			let [count, [cmd, ...args]] = parseCommand(s.slice(1));
			let allMsgs = MessageList.getMessages(channel.id).toArray();
			let msgs = allMsgs.filter(msg => msg.author.id === user.id && msg.state === "SENT").reverse().slice(0, count || 1);
			
			if(cmd === "") throw new SyntaxError("No command given!");

			if("substitute".startsWith(cmd)) {
				if(args.length < 2 || args.length > 3) throw new SyntaxError("Wrong number of arguments");
				let [from, to, flg=""] = args;
				for(let msg of msgs) {
					let c = msg.content.replace(new RegExp(from, flg), to);
					MessageTools.editMessage(channel.id, msg.id, { content: c });
				}
			} else

			if("delete".startsWith(cmd)) {
				if(args.length != 0) throw new SyntaxError("Wrong number of arguments");
				let delAll = msgs => {
					HTTP.delete("/channels/" + channel.id + "/messages/" + msgs[0].id)
						.then(() => {
							if(msgs.length > 1) delAll(msgs.slice(1));
						}, e => {
							if(e.status == 429)
								setTimeout(() => delAll(msgs), e.body.retry_after);
						});
				};
				delAll(msgs);
			} else

			if("nickname".startsWith(cmd)) {
				if(count !== undefined) throw new SyntaxError("Can't count nicks");
				if(args.length > 1) throw new SyntaxError("Wrong number of arguments");
				NicknameTools.changeNickname(channel.getGuildId(), channel.id, "@me", args[0] || "");
			} else

			if("react".startsWith(cmd)) {
				if(args.length < 1) throw new SyntaxError("Wrong number of arguments");
				let emojiContext = Emojis.getDisambiguatedEmojiContext(channel.getGuildId());
				if(MessageList.hasPresent(channel.id)) {
					let [msg] = allMsgs.slice(-(count || 1));
					if(msg && msg.id) {
						let parseEmoji = s => {
							let match = s.match(/^:([^\s:]+?(?:::skin-tone-\d)?):$/);
							return match && emojiContext.getByName(match[1]);
						};
						let parseCEmoji = s => {
							let match = s.match(/^<(a)?:(\w+):(\d+)>$/);
							return match && emojiContext.getById(match[3]);
						};
						let parsed = args.map(s => [s, parseEmoji(s) || parseCEmoji(s)]);
						let failed = parsed.filter(([, a]) => !a);
						if(failed.length)
							throw new SyntaxError("Invalid emoji: " + failed.map(([inp]) => "`" + inp + "`").join(" "));
						else {
							let emojiExists = ({surrogates, name, id}) => msg.reactions.some(({emoji: {name: n, id: i}, me}) => me && ((surrogates == n) || (name == n && id == i)));
							let updateAll = emojis => {
								let e = emojis[0][1];
								let method = (emojiExists(e) ? HTTP.delete : HTTP.put);
								let name = encodeURIComponent(e.id ? e.name + ":" + e.id : e.surrogates);
								method("/channels/" + channel.id + "/messages/" + msg.id + "/reactions/" + name + "/@me")
									.then(() => {
										if(emojis.length > 1) updateAll(emojis.slice(1));
									}, e => {
										if(e.status == 429)
											setTimeout(() => updateAll(emojis), e.body.retry_after);
									});
							};
							updateAll(parsed);
						}
					}
				}
			} else

				throw new SyntaxError("Unknown command");
			return {content: "", tts: false, invalidEmojis: []};
		} catch(e) {
			if(e instanceof SyntaxError)
				Chat.sendBotMessage(channel.id, e.toString() + "\n```" + s + "```");
			else throw e;
		}
	}
})();
