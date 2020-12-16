super: self: {
	mkPatch = file: lineno: text: from: to: super.writeTextFile {
		name = "${file}.patch";
		text = let
			linestr = toString lineno;
			line1 = builtins.replaceStrings ["«»"] [from] text;
			line2 = builtins.replaceStrings ["«»"] [to] text;
		in "--- a/${file}\n+++ b/${file}\n@@ -${linestr},1 +${linestr},1 @@\n-${line1}\n+${line2}\n";
	};

	addSetupPy =
		{ src
		, _basename ? super.lib.removeSuffix ".py" (baseNameOf src)
		, name ? _basename
		, version ? "0.0"
		, preConfigure ? ""
		, ...}@attrs: attrs // {
			inherit name version src;
			doCheck = false;
			unpackPhase = "cp ${src} $(stripHash ${src})";
			preConfigure = preConfigure + ''
				cat >setup.py <<EOF
import setuptools; setuptools.setup(name="${name}", version="${version}", py_modules=["${_basename}"])
EOF
			'';
		};

	icebar = super.python3Packages.callPackage ./icebar { };
	simplei3 = super.python3Packages.callPackage ./simplei3.nix { };
	simplealsa = super.python3Packages.callPackage ./simplealsa.nix { };
}
