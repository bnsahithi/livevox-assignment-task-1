import pytest
import os
def pytest_addoption(parser):
    parser.addoption("--string_value", action="store", default=None, help="Specify a string value")

@pytest.fixture(scope="module")
def account_details_livevox_user1():
   aws_access_key_id=os.environ['aws_access_key_id']
   aws_secret_access_key=os.environ['aws_secret_access_key']
   region_name="ap-south-1"
   auto_scaling_grp_name="lv-test-cpu"   
   return [aws_access_key_id,aws_secret_access_key,region_name,auto_scaling_grp_name]

@pytest.fixture(scope="module")
def account_details_livevox_user2():
   aws_access_key_id=os.environ['aws_access_key_id']
   aws_secret_access_key=os.environ['aws_secret_access_key']
   region_name="us-east-2"
   auto_scaling_grp_name="lv-test-cpu-1"   
   return [aws_access_key_id,aws_secret_access_key,region_name,auto_scaling_grp_name]

@pytest.fixture
def account_details(request):
    value = request.config.getoption("--string_value")
    if value == "user1":
        return request.getfixturevalue("account_details_livevox_user1")
    elif value == "user2":
        return request.getfixturevalue("account_details_livevox_user2")
    else:
        raise ValueError(f"No Account Data specified found for string value: {value}")
     
     


