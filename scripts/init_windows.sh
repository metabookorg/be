# - move to main folder

# - build Virtualenv inside venv folder
py -m venv ./venv

# - activate virtualenv
./venv/Scripts/activate.bat

# - install package
pip install -e .

# - install requirements
pip install -r ./workspace/requirements.txt

# - run main
py workspace