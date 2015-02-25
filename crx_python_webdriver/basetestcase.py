import unittest
import sys
import os

from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

from conf import settings


def make_blocking(fd):
    import fcntl
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    if flags & os.O_NONBLOCK:
        fcntl.fcntl(fd, fcntl.F_SETFL, flags & ~os.O_NONBLOCK)


class BaseTestCase(unittest.TestCase):

    def setUp(self):

        try:
            make_blocking(sys.stdin.fileno())
            make_blocking(sys.stdout.fileno())
        except ImportError:
            pass

        self.driver = settings.DRIVER()
        self.driver.implicitly_wait(settings.IMPLICITLY_WAIT)
        self.base_url = settings.BASE_URL
        self.verification_errors = []
        self.accept_next_alert = True

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to.alert()
        except NoAlertPresentException:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verification_errors)

    def navigate_to(self, path=None):
        path = path or ''
        self.driver.get(self.base_url + "/" + path)


if __name__ == "__main__":
    unittest.main()
