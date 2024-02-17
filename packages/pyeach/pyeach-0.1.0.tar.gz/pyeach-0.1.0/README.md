# pyeach

This is a package meant for use within Cone Health's Enterprise Analytics teams. The goal of this package is to provide reusable python functionality for enterprise projects.

# Developers and Maintainers
[Tyler Ursuy](mailto:tyler.ursuy@conehealth.com)
[Luke Brantley](mailto:luke.brantley@conehealth.com)

# Installation Options
Installation can only be done from [TestPyPi](https://test.pypi.org/project/pyeach/) currently, but will soon be available in a full release at PyPi.

TestPyPi: `pip install -i https://test.pypi.org/simple/ pyeach`

# Build Steps

## TestPyPi
Update pyproject.toml with new version number and execute all commands from the project base directory. Build the .tar and .whl files by executing `python -m build`. Test the package before uploading it to TestPyPi by installing the built pyeach-x.x.x.tar.gz file from the dist folder in a virtual environment and performing the appropriate tests. Install the new test version in a virtual environment with `pip install PATH` where PATH is the absolute path to the tar.gz file. After confirming the package works as intended, execute `python -m twine upload --repository testpypi dist/pyeach-x.x.x.tar.gz dist/pyeach-x.x.x-py3-none-any.whl` to upload the new version to TestPyPi. A prompt for a username and password will appear. Username is `__token__` and your password is your unique TestPyPi API token. A TestPyPi account with MFA is required to generate a token. Register for an account [here](https://test.pypi.org/account/register/).