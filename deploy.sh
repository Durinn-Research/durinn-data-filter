rm -rf dist build *.egg-info
python -m build

python -m pip install twine build

twine check dist/*
twine upload dist/*
