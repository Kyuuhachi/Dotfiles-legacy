#!/usr/bin/env python3
import tempfile
import optimizejars
import subprocess
from pathlib import Path

inject = []
p = Path(__file__).parent.absolute()
def chrome(path):
	inject.append("Services.scriptloader.loadSubScriptWithOptions(%r, {target: window, ignoreCache: true});" % str(p/path))
def content(path):
	inject.append("window.messageManager.loadFrameScript(%r, true);" % str(p/path))

# chrome("userChrome.js")
# content("userContent.js")
inject = []
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')
inject.append('console.log("a")')
inject.append('console.log("aa")')
inject.append('console.log("aaa")')

sep = b"\n//Haxx\n"

def modify(name, buf):
	if name == b"chrome/browser/content/browser/browser.js":
		print("patching")
		return buf.replace(b"""XPCOMUtils.defineLazyGetter(this, "gCustomizeMode", () => {""", b"""XPCOMUtils.defineLazyGetter(this, "gCustomizeMode", () => { console.log('asdf'); """)
	return buf

with tempfile.TemporaryDirectory() as dir:
	dir = Path("/tmp/omni")
	optimizejars.optimizejar("omni.ja", dir/"omni.ja", modify)
	subprocess.check_call(["sudo", "cp", "-v", dir/"omni.ja", "/usr/lib/firefox/browser/omni.ja"])
