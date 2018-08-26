/* global Modules, MonkeyPatch, Renderer, ReactComponents */
"use strict";
(async function() {
	const userToString = u => `<@!${u.id}>`;
	const roleToString = r => `<@&${r.id}>`;
	const chanToString = c => `<#${c.id}>`;
	const emojiToString= e => e.id ? `<${e.animated ? "a" : ""}:${e.originalName || e.name}:${e.id}>` : `:${e.uniqueName}:`;

	const {ComponentDispatch} = await Modules.byFields("ComponentDispatch");
	const {typing} = await Modules.byFields("typing");

	const Preprocessor = Modules.byFields("createBotMessage", "parse", "unparse");
	MonkeyPatch(Preprocessor, "parse", { instead: ({args: [_, s]}) => ({ content: s, tts: false, invalidEmojis: [] }) });
	MonkeyPatch(Preprocessor, "unparse", { instead: ({args: [s]}) => s });

	const TextField = await Modules.byPrototypeFields("selectAutocompletion");
	MonkeyPatch(TextField.prototype, "selectAutocompletion", { instead: ({that, args: [n]}) => {
		let type = that.state.autocompleteType;
		let completers = {
			MENTIONS: (n, {users, globals, roles}) => {
				if(n < users.length) return userToString(users[n].user); else n -= users.length;
				if(n < globals.length) return globals[n].text; else n -= globals.length;
				if(n < roles.length) return roleToString(roles[n]); else return "";
			},
			CHANNELS: (n, {channels}) => chanToString(channels[n]),
			EMOJI: (n, {emoji}) => emojiToString(emoji[n]),
			COMMAND: that.props.autocompleteOptions.COMMAND.getText,
		};
		if(type != null && completers[type] != null) {
			let text = completers[type](n, that.props.autocompletes);
			if(text != null) that.insertText(text, false);
		}
	} });
	MonkeyPatch(TextField.prototype, "handleSelectEmoji", { instead: ({that, args: [e]}) => {
		if(e != null) that.insertText(emojiToString(e));
		that.focus();
	} });
	Renderer.rebindMethods(TextField, "selectAutocompletion", "handleSelectEmoji");

	const UserMentionItem = Modules.find(a => a.displayName == "UserMentionItem");
	MonkeyPatch(UserMentionItem.prototype, "handleMention", { instead: ({that}) => {
		Modules.byFields(["dispatch"]).dispatch({ type: "CONTEXT_MENU_CLOSE" });
		ComponentDispatch.dispatchToLastSubscribed("INSERT_TEXT", { content: userToString(that.props.user) });
		if(that.state.channelId != null) typing(that.state.channelId);
	} });
	Renderer.rebindMethods(UserMentionItem, "handleMention");

	const Message = ReactComponents.get("Message");
	MonkeyPatch(Message.prototype, "handleUsernameClick", { instead: ({that, args: [e, msg]}) => {
		if(e.shiftKey && !msg.author.isNonUserBot()) {
			ComponentDispatch.dispatchToLastSubscribed("INSERT_TEXT", { content: userToString(msg.author) });
			if(that.props.channel.id != null) typing(that.props.channel.id);
			e.preventDefault();
			e.stopPropagation();
		}
	} });
	Renderer.rebindMethods(Message, "handleUsernameClick");

	// There's nother class calling INSERT_TEXT (5750), but I haven't managed
	// to get an instance. I have no idea what that class even is, either.
})();
