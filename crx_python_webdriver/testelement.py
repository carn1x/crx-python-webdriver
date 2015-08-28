import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import time
from conf import settings
import testassertions as a


class TestElement:
    selector = None
    select_method = None
    driver = None
    testcase = None
    name = None

    def __init__(self, selector, select_method, driver, testcase, name=None):
        self.selector = selector
        self.select_method = select_method
        self.driver = driver
        self.testcase = testcase
        self.name = name
        self.find_displayed = False
        time.sleep(settings.PER_COMMAND_DELAY)

    def select(self, override_selector=None, override_method=None):
        selector = override_selector or self.selector
        method = override_method or self.select_method

        by = self.get_locator_by(method)

        if not self.find_displayed:
            return self.driver.find_element(by=by, value=selector)
        else:
            elements = self.driver.find_elements(by=by, value=selector)
            for element in elements:
                if element.is_displayed():
                    return element

    def get_locator_by(self, method=None):
        method = method or self.select_method

        by = None

        if method == 'id':
            by = By.ID

        elif method == 'xpath':
            by = By.XPATH

        elif method == 'css':
            by = By.CSS_SELECTOR

        elif method == 'name':
            by = By.NAME

        elif method == 'link_text':
            by = By.LINK_TEXT

        elif method == 'partial_link_text':
            by = By.PARTIAL_LINK_TEXT

        else:
            print 'Unknown method: %s' % method

        return by

    def locator(self):
        return self.get_locator_by(), self.selector

    def assert_(self, assertions, values=None, find_displayed=False):
        """
        :assertions
            A list of keys for which to apply assertions.
            Defaults to check if the element is present.
        """
        self.find_displayed = find_displayed

        assertions = assertions or [a.PRESENT]
        for assertion in assertions:
            if assertion == a.WAIT:
                self.select()

            elif assertion == a.PRESENT:
                self.testcase.assertTrue(self.select_quick())

            elif assertion == a.NOT_PRESENT:
                self.testcase.assertFalse(self.select_quick())

            elif assertion == a.ENABLED:
                self.testcase.assertTrue(self.select_quick().is_enabled())

            elif assertion == a.DISABLED:
                self.testcase.assertFalse(self.select_quick().is_enabled())

            elif assertion == a.CHECKED:
                self.testcase.assertTrue(self.select_quick().is_selected())

            elif assertion == a.UNCHECKED:
                self.testcase.assertFalse(self.select_quick().is_selected())

            elif assertion == a.TEXT:
                self.testcase.assertRegexpMatches(self.select_quick().text, values[assertion])

            elif assertion == a.CONTAINS:
                self.testcase.assertIn(values[assertion], self.select_quick().text)

            elif assertion == a.NOT_CONTAINS:
                self.testcase.assertNotIn(values[assertion], self.select_quick().text)

            elif assertion == a.CLASS:
                self.testcase.assertTrue(values[assertion] in self.select_quick().get_attribute('class'))

            elif assertion == a.DISPLAYED:
                self.testcase.assertTrue(self.select_quick().is_displayed())

            elif assertion == a.NOT_DISPLAYED:
                self.testcase.assertFalse(self.select_quick().is_displayed())

            elif assertion == a.GTE:
                self.testcase.assertTrue(int(self.select_quick().text) >= values[assertion])

            elif assertion == a.LTE:
                self.testcase.assertTrue(int(self.select_quick().text) <= values[assertion])

            elif assertion == a.EXPECTED_INVISIBLE:
                try:
                    WebDriverWait(self.driver, settings.IMPLICITLY_WAIT).until(
                        expected_conditions.invisibility_of_element_located((self.locator()))
                    )
                finally:
                    pass

            elif assertion == a.EXPECTED_VISIBLE:
                try:
                    WebDriverWait(self.driver, settings.IMPLICITLY_WAIT).until(
                        expected_conditions.visibility_of_element_located((self.locator()))
                    )
                finally:
                    pass

            elif assertion == a.SELECTED_OPTION:
                selected_option = Select(self.select_quick()).first_selected_option
                self.testcase.assertNotEqual(values[assertion], selected_option.get_attribute('value'))

            else:
                raise Exception('AssertElement unknown assertion: %s' % assertion)

    def select_quick(self):
        """
        Overrides the driver implicit timeout so it can fail fast as well as
        catch exception so negative assertions can be made.
        """
        self.driver.implicitly_wait(settings.IMPLICITLY_WAIT_QUICK_ASSERT)
        select = None

        # TODO: Narrow the expected Exceptions.
        try:
            select = self.select()
        except Exception:
            pass

        self.driver.implicitly_wait(settings.IMPLICITLY_WAIT)
        return select

    def capture(self, pattern=None, result_index=None, _property=None, _property_key=None):
        """
        :pattern
            Regex pattern to match against the text of the selected element.
        :result_index
            Index of the pattern match result to return, defaults to 1.
        :_property
            The property of which to match against.
        :_property_key
            The key of the _property to match against.
            e.g.: _property = attr, _property_key = href
        """
        result_index = result_index or 1
        _property = _property or 'text'
        _property_key = _property_key or None

        text = ''
        if _property == 'text':
            text = self.select().text
        elif _property == 'attr':
            text = self.select().get_attribute(_property_key)

        if not pattern:
            pattern = '.*'
            result_index = 0
        m = re.search(pattern, text)
        if m and m.group(result_index):
            return m.group(result_index)
        else:
            raise Exception('ReturnElement can not find "%s" in "%s"' % (pattern, text))

    def input(self, value=None):
        self.select().clear()
        self.select().send_keys(value)

    def click(self, value=None):
        self.select().click()

    def submit(self, value=None):
        self.select().submit()

    def select_by(self, select_by, value):
        if select_by == 'text':
            print 'selecting %s by %s' % (value, select_by)
            element = self.select()
            Select(element).select_by_visible_text(value)

        if select_by == 'ufd':
            # A select element overridden by the Unobstrusive Filter Dropdown which
            # requires interaction with multiple click events.
            self.select().click()
            self.select(value, select_by).click()

    def hover(self, value=None):
        ActionChains(self.driver).move_to_element(self.select()).perform()

    def hover_click(self, value=None):
        ActionChains(self.driver).move_to_element(self.select()).click().perform()

    def drag_to(self, destination):
        source = self.select()
        source_location = source.location
        dest_location = destination.select().location
        offset_x = dest_location['x'] - source_location['x']
        offset_y = dest_location['y'] - source_location['y']
        if offset_y < 0:
            offset_y -= 1
        elif offset_y > 0:
            offset_y += 1
        ActionChains(self.driver).drag_and_drop_by_offset(source, offset_x, offset_y).perform()

    def text(self, value=None):
        return self.select_quick().text

    def get_text(self, element, index=None):
        """
        TODO: Remove, deprecated.
        """
        return self.text(element, index=index)
