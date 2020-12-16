#!/usr/bin/env python3
import setuptools

setuptools.setup(
	name="icebar",
	version="1.1",
	author="Kyuuhachi",

	packages=setuptools.find_packages(),
	entry_points={
		"gui_scripts": [ "icebar=icebar.bar:main" ]
	},

	platforms="any",
	python_requires=">=3.8",
	install_requires=["pygobject", "appdirs"],
)
