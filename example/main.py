import unittest
import sys
from crx_python_webdriver.basetestcase import BaseTestCase
from scripts.TestHomePage import TestHomePage
from scripts.TestSignIn import TestSignIn

args = []


class Tests(BaseTestCase):
    def setUp(self):
        super(Tests, self).setUp()

        # Here we can access arguments passed by accessing the `args` list
        # if args: doSomething(args)

    def test__home__logo(self):
        TestHomePage(self).test_logo()

    def test__home__signin(self):
        TestSignIn(self).test_sign_in()


if __name__ == "__main__":
    # Capture all commandline args for usage in Tests.setUp(), then trim sys.argv so unittest doesn't get angry.
    args.extend(sys.argv[1:])
    sys.argv = sys.argv[:1]

    unittest.main()
