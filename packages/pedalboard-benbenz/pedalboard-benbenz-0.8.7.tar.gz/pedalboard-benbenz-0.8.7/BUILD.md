Check [contributing]()

```
git clone --recurse-submodules --shallow-submodules git@github.com:benbenz/pedalboard.git
cd pedalboard
##### DONT USE
##### nix-shell --pure
python -m venv .venv
source .venv/bin/activate
pip3 install pybind11 tox twine

# BUILD
pip3 install .
# OR
python3 setup.py build_ext --inplace

# PACKAGE+UPLOAD
python setup.py sdist
python -m twine upload dist/*
```