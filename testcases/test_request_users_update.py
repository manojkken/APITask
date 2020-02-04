from unittest_data_provider import data_provider

from testlib.requests.request_data_generators import requestDataGenerator
from testlib.requests.request_main_test import *


class requestUsersUpdateTests(requestMainTestCase):
    @data_provider(requestDataGenerator.provide_users())
    def test_update_user(self, param):
        data = {"name": "morpheus", "job": "leader"}
        response = self.send_api_request(f'{self.request_endpoint}/{param}', self.request_type_put,
                                         data=json.dumps(data)
                                         )
        self.assert_code_ok(response)
