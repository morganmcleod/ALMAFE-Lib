python -m pip install --upgrade setuptools wheel
python setup.py clean --all
del /Q dist\*.*
python setup.py sdist bdist_wheel
