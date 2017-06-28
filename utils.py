import os, yaml, requests, logging, json

current_path = os.getcwd()
workspace_name = 'python_api_test'
workspace_path = current_path[:current_path.index(workspace_name) + len(workspace_name)]

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('Utils')


def get_api_requests_data(file_path, form_data_part='form_data'):
    """Get the api requests data from config file.
    get the request method
    get the request url
    get the request server type
    get the request form data
    :param file_path: pass the api request config file path
    :return:
        yaml_data: all yaml data
        api_method: request method
        api_url: request url
        api_form_data: request data
    """
    file_path = get_yaml_path(file_path)[1]
    yaml_data = get_yaml_data(file_path)
    api_method = yaml_data['method']
    api_url = yaml_data['url']
    server_type = get_api_server()[0]
    api_form_data = yaml_data[form_data_part][server_type]['data']
    return yaml_data, api_method, api_url, api_form_data, server_type


def get_api_response_data(file_path, response_data_part='response_data'):
    file_path = get_yaml_path(file_path)[1]
    yaml_data = get_yaml_data(file_path)
    server_type = get_api_server()[0]
    return yaml_data[response_data_part][server_type]['data']


def encrypt_requests_data(api_form_data, token):
    data = cal_base64(api_form_data)
    sign = cal_md5(data + token)
    return {'data': data, 'sign': sign}


def send_requests_with_original_data(file_path, form_data_part='form_data', need_token=True):
    return send_requests_with_yaml_data(file_path, form_data_part=form_data_part, need_token=need_token)


def send_requests_with_modified_data(file_path, modified_data, form_data_part='form_data', need_token=True):
    return send_requests_with_yaml_data(file_path, modified_data=modified_data, form_data_part=form_data_part,
                                        need_token=need_token)


def send_requests_with_yaml_data(file_path, form_data_part='form_data', modified_data=None, need_token=True):
    requests_data = get_api_requests_data(file_path, form_data_part)
    url = get_api_server()[1] + requests_data[2]
    log.debug('api url: ' + url)
    method = requests_data[1]
    log.debug('api method: ' + method)
    if modified_data is None:
        requests_form_data = requests_data[3]
        log.debug('original requests data: ' + json.dumps(requests_form_data))
    else:
        requests_form_data = modified_data
        log.debug('modified requests data: ' + json.dumps(requests_form_data))
    token = get_temp_token()
    log.debug('token: ' + token)
    params = encrypt_requests_data(requests_form_data, token)
    log.debug('encrypted data: ' + json.dumps(params))
    if need_token:
        headers = {'token': get_temp_token(), 'Content-Type': 'application/x-www-form-urlencoded'}
    else:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return send_requests_data(method, url, headers, params)


def send_requests_data(method, url, headers, data):
    return requests.request(method, url, headers=headers, data=data, verify=False)


def get_yaml_data(file_path):
    stream = open(file_path, 'r', encoding='utf-8')
    yaml_data = yaml.load(stream)
    stream.close()
    return yaml_data


def get_yaml_path(file_path):
    base_path = workspace_path + '/configs'
    file_name = file_path.split('/')[-1].split('.')[0]
    full_file_path = base_path + file_path
    return file_name, full_file_path


def get_api_server():
    file_path = get_yaml_path('/config.yaml')[1]
    yaml_data = get_yaml_data(file_path)
    server_type = yaml_data['server_type']
    return server_type, yaml_data[server_type + '_server']


def append_data_to_yaml(file_path, data):
    write_data_to_yaml(file_path, data, 'a')


def save_data_to_yaml(file_path, data):
    write_data_to_yaml(file_path, data, 'w')


def write_data_to_yaml(file_path, data, mode):
    stream = open(file_path, mode)
    yaml.dump(data, stream, default_flow_style=False)
    stream.close()


def update_value_to_yaml(file_path, key, value):
    file_path = get_yaml_path(file_path)[1]
    data = get_yaml_data(file_path)
    data[key] = value
    stream = open(file_path, 'w')
    yaml.dump(data, stream, default_flow_style=False)
    stream.close()


def update_value_to_temp_config(key, value):
    update_value_to_yaml('/temp.yaml', key, value)


def append_temp_config(data):
    append_data_to_yaml(get_yaml_path('/temp.yaml')[1], data)


def append_data_to_temp_config(key, value):
    append_temp_config({key: value})


def append_token_to_temp_config(token_value):
    append_temp_config({'token': token_value})


def get_temp_token():
    yaml_data = get_yaml_data(get_yaml_path('/temp.yaml')[1])
    try:
        return yaml_data['token']
    except:
        log.debug('not found the key token')
        return ''


# encrypt method for send the requests
def cal_base64(data):
    import base64
    data_bytes = base64.b64encode(bytes(str(json.dumps(data)), 'utf-8'))
    return str(data_bytes).split('\'')[1]


def cal_md5(data):
    import hashlib
    md = hashlib.md5(data.encode('utf-8'))
    return md.hexdigest()


def cal_api_request(data_str, token):
    return cal_base64(data_str), cal_md5(data_str + token)


def generate_results(pytest_scope=workspace_path + '/tests', results_dir=workspace_path + '/report'):
    # invoke_command('pytest ' + pytest_scope + ' --alluredir ' + results_dir)
    import pytest
    pytest.main([pytest_scope, '--alluredir=' + results_dir])


def generate_html_report(results_dir=workspace_path + '/report', html_report_dir=workspace_path + '/report/html'):
    cmd = 'allure generate ' + results_dir + ' -o ' + html_report_dir
    log.debug(cmd)
    os.system(cmd)


def invoke_command(command):
    import platform
    platform_sys = platform.system().lower()
    if platform_sys == 'windows':
        cmd = 'python -m ' + command
        log.debug(cmd)
        os.system(cmd)
    elif platform_sys == 'linux' or platform_sys == 'linux2':
        cmd = 'python3 -m ' + command
        log.debug(cmd)
        os.system(cmd)
    elif platform_sys == 'darwin':
        cmd = 'python3 -m ' + command
        log.debug(cmd)
        os.system(cmd)


def generate_random_characters(length, type='string'):
    import random, string
    if type == 'string':
        str = ''
        for i in range(length):
            str += random.choice(string.ascii_letters + string.digits)
        random_results = str
    if type == 'int':
        range_start = 10 ** (length - 1)
        range_end = (10 ** length) - 1
        random_results = random.randint(range_start, range_end)
    if type == 'chinese':
        str = ""
        for i in range(length):
            str += chr(random.randint(0x4E00, 0x9FA5))
        random_results = str
    return random_results
