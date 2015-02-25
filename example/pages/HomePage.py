from crx_python_webdriver.testassertions import DISPLAYED
from crx_python_webdriver.testpage import TestPage


class HomePage(TestPage):

    @classmethod
    def get_definitions(cls):
        return {
            # `goto` should be defined for each page defined.
            'goto': {
                'value': '',
            },

            # If a string is provided, then CSS type selector is assumed.
            'logo': 'a.header-logo-wordmark',

            # Alternatively XPath selectors can be used.
            'header sign in': {
                'method': 'xpath',
                'selector': '//div[@class="header header-logged-out"]'
                            '//div[@class="header-actions"]/'
                            'a[text()[contains(.,"Sign in")]]'
            }
        }

    def assert_logo(self):
        self.assert_('logo', assertions=[DISPLAYED])

    def assert_sign_in(self):
        self.assert_('header sign in', assertions=[DISPLAYED])

    def click_logo(self):
        self.click('logo')

    def click_sign_in(self):
        self.click('header sign in')
