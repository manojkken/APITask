import sys
import unittest
from utils.suite_maker import SuiteMaker

tests_module = 'testcases'
loader = unittest.TestLoader()
suite = SuiteMaker.make_suite(loader, tests_module)
runner = unittest.TextTestRunner()
result = runner.run(suite)
exit_code = 0 if len(result.errors) + len(result.failures) == 0 else 1
sys.exit(exit_code)
