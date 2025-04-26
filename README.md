1. Need to install requirements.txt
2. Navigate to tests root directory


run api tests -
python -m pytest api_project/tests/test_pet_store.py -vv

run ui tests
CONFIG=use_insider_config pytest --driver Chrome --driver-path PATH_TO_YOUR_CHROMEDRIVER ui_test_project/tests/test_insider_careers.py -vv

