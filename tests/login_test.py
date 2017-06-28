import logging
import time
import pytest
import allure
from utils import send_requests_with_original_data, append_token_to_temp_config, get_api_server, get_api_response_data, \
    update_value_to_temp_config
from base_test import BaseTest

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Test_Login')
time.sleep(1)

file_rel_path = '/user/login.yaml'


@pytest.allure.severity(pytest.allure.severity_level.CRITICAL)
@allure.feature('user')
@allure.story('login')
class Test_Login(BaseTest):
    @pytest.mark.first
    @allure.step(title="test_login01_success")
    def test_login01_success(self):
        allure.attach('description', 'login success')
        response = send_requests_with_original_data(file_rel_path, need_token=False)
        json_data = response.json()
        log.debug(json_data)
        response_data = get_api_response_data(file_rel_path)
        assert response.status_code == 200
        assert json_data['message'] == '成功'
        assert json_data['code'] == '10000'
        # save token to config temp
        update_value_to_temp_config('token', json_data['responseBody']['token'])
        # check uid
        assert json_data['responseBody']['uid'] == response_data['uid']
        # check checkStatus
        assert json_data['responseBody']['checkStatus'] == response_data['checkStatus']
        # check name
        assert json_data['responseBody']['name'] == response_data['name']

    @allure.step(title="test_login02_invalid_user")
    def test_login02_invalid_user(self):
        allure.attach('description', 'login invalid user')
        response = send_requests_with_original_data(file_rel_path, 'form_data_invalid_user')
        json_data = response.json()
        log.debug(json_data)
        response_data = get_api_response_data(file_rel_path, 'response_data_invalid_user')
        assert response.status_code == 200
        assert json_data['message'] == response_data['message']
        assert json_data['code'] == response_data['code']

    @allure.step(title="test_login03_invalid_password")
    def test_login03_invalid_password(self):
        allure.attach('description', 'login invalid password')
        response = send_requests_with_original_data(file_rel_path, 'form_data_invalid_password')
        json_data = response.json()
        log.debug(json_data)
        response_data = get_api_response_data(file_rel_path, 'response_data_invalid_password')
        assert response.status_code == 200
        assert json_data['message'] == response_data['message']
        assert json_data['code'] == response_data['code']
