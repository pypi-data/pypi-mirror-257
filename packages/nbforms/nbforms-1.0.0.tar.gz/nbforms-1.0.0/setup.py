import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

with open("nbforms/version.py") as f:
	env = {}
	exec(f.read(), env)
	version = env["__version__"]

setuptools.setup(
	name = "nbforms",
	version = version,
	author = "Chris Pyles",
	author_email = "cpyles@berkeley.edu",
	description = "Jupyter Notebook forms using ipywidgets",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/chrispyles/nbforms",
	license = "BSD-3-Clause",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
	]
)
