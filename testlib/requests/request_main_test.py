from testlib.main_test_case import *


class requestMainTestCase(MainTestCase):
    request_endpoint = 'users'

    def setUp(self):
        super().setUp()

    @classmethod
    def preparations_before_tests(cls):
        super().preparations_before_tests()

    @classmethod
    def read_tests_config(cls):
        super().read_tests_config()
        cls.cfg_host = cls.config['typiCode']['host']

    def get_request_url(self, request):
        return f'/{request}'

    def send_api_request(self, request, request_type, params=None, decode_resp=True, data=None,
                         headers=None, need_headers=False):
        request = self.get_request_url(request)
        return self.make_request(request=request,
                                 params=params,
                                 headers=headers,
                                 decode_resp=decode_resp,
                                 request_type=request_type,
                                 data=data,
                                 need_headers=need_headers)
