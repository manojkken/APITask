import os
import re
from importlib import import_module


class SuiteMaker:

    @staticmethod
    def make_suite(loader, tests_package):
        tests = SuiteMaker.get_tests_files(package=tests_package)
        suite = loader.loadTestsFromModule(tests_package)
        for test in tests:
            mod = import_module(test)
            suite.addTests(loader.loadTestsFromModule(mod))
        return suite

    @staticmethod
    def get_tests_files(package):
        tests = []
        tests_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not tests_path.endswith('/'):
            tests_path = f'{tests_path}/'
        all_files = os.listdir(tests_path + package)
        for c_file in all_files:
            if c_file.startswith('.') or c_file.startswith('_'):
                continue
            c_file = package + '.' + re.sub('(\.py$|\.pyc$)', '', c_file)
            if c_file not in tests:
                tests.append(c_file)
        return tests
