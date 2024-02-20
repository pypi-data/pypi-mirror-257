Installation
************

Simple pip install should work, but we recommend to do so in a clean conda environment, as follows:

* ``conda create -n pylanetary-tester python=3.11`` (or any Python from 3.9 to 3.12)
* ``conda activate pylanetary-tester``
* ``pip install pylanetary``
	
Troubleshooting
~~~~~~~~~~~~~~~
Here we attempt to document install issues people have had, and their solutions.
Note that many of these issues pre-date the current version of pylanetary, and only arose due to the prior need
to download requirements.txt, which is no longer necessary for installation.

* requirements.txt not found. Most likely, you never downloaded requirements.txt, or you are not running pip install -r requirements.txt in the same folder where you put requirements.txt
* pip install requirements.txt fails instantly with a crazy-looking error message. Try opening requirements.txt, and check that its just ten or so lines of human-readable text. If it's some huge html soup, that means you didn't use the "download raw" button when downloading
* dependency conflicts when running pip install. Try using the option --force-reinstall, e.g., ``pip install --force-reinstall -r requirements.txt``
* dependency conflicts persist after force-reinstall. Check that your conda is working right. When this happened to a colleague, we found that ``which conda`` was returning some ten-line thing with a bunch of brackets instead of just the directory where conda lived. Solution was eventually to manually ``pip install filelock`` and ``pip install jsonschema``
* import error in utils ``version 'GLIBCXX_3.4.30' not found (required by .../scipy/spatial/fft/)``. This likely means your python version is not at least 3.9.