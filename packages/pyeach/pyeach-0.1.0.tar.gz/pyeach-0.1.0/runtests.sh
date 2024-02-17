echo 'Performing unit tests.'

python -m unittest

echo 'All unit tests successfull.'
echo 'Building pyeach'

python -m build

echo 'pyeach successfully built.'
echo 'Creating venv'

python -m venv venv
source venv/Scripts/activate
pip install dist/pyeach-0.0.4.tar.gz

echo 'pyeach successfully installed.'
echo 'Removing venv.'

rm -r venv

echo 'Done.'