import configparser
import json
import os
import unittest
import uuid
from datetime import datetime
from optparse import OptionParser

import requests

from utils.logger import Logger


class MainTestCase(unittest.TestCase):
    config_file_path = '../config'
    config_file_name = 'config.ini'
    cfg_logs_dir = ''
    unique_id = ''

    test_name = ''
    host = ''
    cfg_host = ''

    status_code_not_found = 404
    status_code_ok = 200
    status_code_success = 201
    status_code_delete_success = 204

    request_type_get = 'get'
    request_type_post = 'post'
    request_type_put = 'put'
    request_type_delete = 'delete'

    @classmethod
    def setUpClass(cls):
        cls.preparations_before_tests()

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_after_tests()

    def setUp(self):
        self.test_name = self.id().split('.')[-1]
        Logger.log_msg(f"{'=' * 10} Start test: {self.test_name} {'=' * 10}")

    def tearDown(self):
        Logger.log_msg(f"{'=' * 10} Finish test: {self.test_name} {'=' * 10}")

    @classmethod
    def preparations_before_tests(cls):
        cls.unique_id = f'{uuid.uuid4().hex[0:7]}'
        cls.parser = OptionParser()
        cls.define_available_options()
        cls.read_tests_config()
        cls.host = cls.define_host()
        cls.logs_path = cls.define_logs_path()
        Logger.create_logger(f"{cls.logs_path}{cls.__name__}_{datetime.today().strftime('%d%m%y%H%M%S')}.log")
        Logger.log_msg('Starting preparations before tests')

    @classmethod
    def cleanup_after_tests(cls):
        Logger.log_msg('Starting cleanup_after_tests')

    @classmethod
    def define_available_options(cls):
        cls.parser.add_option('-H',
                              '--host',
                              dest='host',
                              help='set host')
        cls.parser.add_option('-l',
                              '--logs-path',
                              dest='logs_path',
                              help='set path to logs dir')

    @classmethod
    def read_tests_config(cls):
        cls.config = configparser.ConfigParser()
        cls.config.read(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), cls.config_file_path, cls.config_file_name))
        cls.cfg_logs_dir = cls.config['main']['logs_dir']

    @classmethod
    def define_host(cls):
        (options, args) = cls.parser.parse_args()
        host = options.host
        if not host:
            host = cls.cfg_host
        return host

    @classmethod
    def define_logs_path(cls):
        (options, args) = cls.parser.parse_args()
        logs_path = options.logs_path
        if not logs_path:
            logs_path = cls.cfg_logs_dir
        if logs_path.startswith('~'):
            logs_path = os.path.expanduser(logs_path)
        if not logs_path.endswith('/'):
            logs_path = f'{logs_path}/'
        return logs_path

    def make_request(self, request=None, params=None, request_type='get', decode_resp=True, need_headers=False,
                     stream=False, url=None, data=None, headers=None, auth=None, files=None):
        response = None
        res = {}
        if not request and not url:
            raise AttributeError('Both attributes request and url are not defined.')
        if not url:
            url = self.get_url(request)
        log_message = self.build_request_log_message(request_type, url, request, params, headers, data, auth, files)
        Logger.log_msg(log_message)
        if request_type == self.request_type_get:
            response = requests.get(url=url,
                                    params=params,
                                    stream=stream,
                                    headers=headers,
                                    auth=auth)
        if request_type == self.request_type_post:
            response = requests.post(url=url,
                                     params=params,
                                     data=data,
                                     headers=headers,
                                     files=files)
        if request_type == self.request_type_put:
            response = requests.put(url=url,
                                    params=params,
                                    data=data,
                                    headers=headers)
        if request_type == self.request_type_delete:
            response = requests.delete(url=url,
                                    params=params,
                                    data=data,
                                    headers=headers)
        res['response'] = response
        res['status'] = response.status_code
        res_msg = f"status code {res['status']}"
        if decode_resp:
            try:
                res['response'] = json.loads(response.content)
            except ValueError:
                res['response'] = response.content
            res_msg += f" {response.content.decode('utf-8')}"
        if need_headers:
            res['headers'] = response.headers
        Logger.log_msg(f'Got response: {res_msg}')
        return res

    def get_url(self, request):
        return self.host + request

    @staticmethod
    def build_request_log_message(request_type, url, request, params, headers, data, auth, files):
        request_log_message = f'Sending {request_type} request: \n url = {url}'
        if not url and request:
            request_log_message += str(request)
        if params:
            request_log_message += f'\n params = {json.dumps(params)}'
        if headers:
            request_log_message += f'\n headers = {headers}'
        if data:
            if isinstance(data, dict):
                data_copy = data.copy()
                for k, v in data_copy.items():
                    if isinstance(v, str) and len(v) > 1000:
                        data_copy[k] = f'First 1000 symbols: {data_copy[k][:1000]}'
                request_log_message += f'\n data = {data_copy}'
            else:
                request_log_message += f'\n data = {data}'
        if auth:
            request_log_message += f'\n auth = {auth}'
        if files:
            if isinstance(files, dict) and isinstance(files['file'][1], bytes) and len(files['file'][1]) > 100:
                request_log_message += f"\n files = {files['file'][0]}"
            else:
                request_log_message += f'\n files = {files}'
        return request_log_message

    def assert_unauthorized_request_code(self, response):
        self.assertEqual(self.status_code_unauthorized, response['status'])

    def assert_not_found_request_code(self, response):
        self.assertEqual(self.status_code_not_found, response['status'])

    def assert_code_ok(self, response):
        self.assertEqual(self.status_code_ok, response['status'])

    def assert_code_success(self, response):
        self.assertEqual(self.status_code_success, response['status'])

    def assert_code_delete_success(self, response):
        self.assertEqual(self.status_code_delete_success, response['status'])
