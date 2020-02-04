from unittest_data_provider import data_provider

from testlib.requests.request_data_generators import requestDataGenerator
from testlib.requests.request_main_test import *


class requestUsersDeleteTests(requestMainTestCase):
    @data_provider(requestDataGenerator.provide_users())
    def test_delete_user(self, param):
        response = self.send_api_request(f'{self.request_endpoint}/{param}', self.request_type_delete
                                         )
        self.assert_code_delete_success(response)
