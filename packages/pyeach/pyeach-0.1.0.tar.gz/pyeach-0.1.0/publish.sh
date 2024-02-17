# Perform tests
bash runtests.sh

# Build pyeach
python -m build

## publish to TestPyPi - only do when version is ready for upload
## replace x.x.x with correct version number
# python -m twine upload --repository testpypi dist/pyeach-0.1.0.tar.gz dist/pyeach-0.1.0-py3-none-any.whl
python -m twine upload --repository dist/pyeach-0.1.0.tar.gz dist/pyeach-0.1.0-py3-none-any.whl