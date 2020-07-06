#!/usr/bin/env python3
import optimizejars
from pathlib import Path
import shutil

with open("/usr/lib/firefox/browser/omni.ja", "rb") as f:
	files = optimizejars.read(f)
out = Path("_data")
if out.is_dir(): shutil.rmtree(out)
for k, v in files.items():
	outp = out / k
	outp.parent.mkdir(parents=True, exist_ok=True)
	outp.write_bytes(v["data"])

with open("/usr/lib/firefox/omni.ja", "rb") as f:
	files2 = optimizejars.read(f)
out = Path("_data2")
if out.is_dir(): shutil.rmtree(out)
for k, v in files2.items():
	outp = out / k
	outp.parent.mkdir(parents=True, exist_ok=True)
	outp.write_bytes(v["data"])
