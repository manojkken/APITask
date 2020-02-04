from unittest_data_provider import data_provider

from testlib.requests.request_data_generators import requestDataGenerator
from testlib.requests.request_main_test import *


class requestUsersGetTests(requestMainTestCase):
    def test_get_users(self):
        response = self.send_api_request(self.request_endpoint, self.request_type_get
                                         )
        self.assert_code_ok(response)
        self.assertEqual(response['response']['per_page'], 6)

    @data_provider(requestDataGenerator.provide_users())
    def test_get_single_user(self, param):
        response = self.send_api_request(f'{self.request_endpoint}/{param}', self.request_type_get
                                         )
        self.assert_code_ok(response)

    def test_get_invalid_user(self):
        response = self.send_api_request(f'{self.request_endpoint}/{51}', self.request_type_get
                                         )
        self.assert_not_found_request_code(response)
