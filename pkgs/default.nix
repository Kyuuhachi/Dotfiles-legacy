super: self: {
	mkPatch = file: lineno: text: from: to: super.writeTextFile {
		name = "${file}.patch";
		text = let
			linestr = toString lineno;
			line1 = builtins.replaceStrings ["«»"] [from] text;
			line2 = builtins.replaceStrings ["«»"] [to] text;
		in "--- a/${file}\n+++ b/${file}\n@@ -${linestr},1 +${linestr},1 @@\n-${line1}\n+${line2}\n";
	};

	icebar = super.python3Packages.callPackage ./icebar { };
}
