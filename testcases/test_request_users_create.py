from testlib.requests.request_main_test import *


class requestUsersCreateTests(requestMainTestCase):
    def test_create_user(self):
        data = {"name": "morpheus", "job": "leader"}
        response = self.send_api_request(self.request_endpoint, self.request_type_post, data=json.dumps(data)
                                         )
        self.assert_code_success(response)
