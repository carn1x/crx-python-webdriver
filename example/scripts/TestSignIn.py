from crx_python_webdriver.testscript import TestScript
from pages.SignInPage import SignInPage


class TestSignIn(TestScript):

    def test_sign_in(self):
        s = SignInPage(self)
        s.goto()

        # Make sure we have a Sign In button.
        s.assert_sign_in()

        # Click it.
        s.click_sign_in()

        # Make sure we still have a Sign In button.
        s.assert_sign_in()

        # Make sure we have a Sign Up button.
        s.assert_sign_up()

        # Click the logo to go to the Homepage.
        s.click_logo()

        # The Sign Up button shouldn't appear on the Homepage, although it is only hidden by CSS.
        s.assert_sign_up_invisible()
