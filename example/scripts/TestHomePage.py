from crx_python_webdriver.testscript import TestScript
from pages.HomePage import HomePage


class TestHomePage(TestScript):

    def test_logo(self):
        h = HomePage(self)
        h.goto()
        h.assert_logo()