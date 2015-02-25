from crx_python_webdriver.testassertions import DISPLAYED, NOT_PRESENT, NOT_DISPLAYED, PRESENT
from pages.HomePage import HomePage


class SignInPage(HomePage):

    @classmethod
    def get_definitions(cls):
        return {
            # This setting will overwrite the `goto` defined in the superclass HomePage.
            'goto': {
                'value': '/login',
            },

            # New definitions will be added to the definitions provided by the superclass HomePage.
            'header sign up': {
                'method': 'xpath',
                'selector': '//div[@class="header header-logged-out"]'
                            '//div[@class="header-actions"]/'
                            'a[text()[contains(.,"Sign up")]]'
            }
        }

    def assert_sign_up(self):
        self.assert_('header sign up', assertions=[DISPLAYED])

    def click_sign_up(self):
        self.click('header sign up')

    def assert_sign_up_invisible(self):
        self.assert_('header sign up', assertions=[PRESENT, NOT_DISPLAYED])

