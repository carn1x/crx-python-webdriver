from testelement import TestElement, a
import time
from conf import settings
from urlparse import urlparse


class TestPage(object):
    driver = None
    testcase = None
    definitions = None
    url = None

    def __init__(self, test_script):
        self.driver = test_script.driver
        self.testcase = test_script.testcase
        self.definitions = {}
        self.definitions = self.get_all_definitions()

    @classmethod
    def get_all_definitions(cls):
        """
        If this is not the base class, then get the definitions from the parent.
        """
        definitions = {}
        while True:
            _definitions = cls.get_definitions()
            _definitions.update(definitions)
            definitions = _definitions
            if cls == TestPage:
                return definitions
            else:
                cls = cls.__bases__[0]

    @classmethod
    def get_definitions(cls):
        return {
            'body': 'body',
        }

    def get_value(self, name):
        if isinstance(self.definitions[name], dict):
            return self.definitions[name].get('value')

    def get_assertions(self, name):
        if isinstance(self.definitions[name], dict):
            return self.definitions[name].get('assertions')

    def get_element(self, name, index=None):
        selector_method = 'css'
        selector = self.definitions[name]

        # If the def is a dict, then extract the details, otherwise the entire def is the selector.
        if isinstance(self.definitions[name], dict):
            selector_method = self.definitions[name].get('method') or selector_method
            selector = self.definitions[name].get('selector')

        if index:
            selector = selector % index

        return TestElement(
            selector,
            selector_method,
            self.driver,
            self.testcase,
            name)

    def command(self, command, element_key, value=None, index=None):
        value = value or self.get_value(element_key)

        if index:
            print '%s %s[%s] : %s' % (command, element_key, index, value)
        else:
            print '%s %s : %s' % (command, element_key, value)
        element = self.get_element(element_key, index=index)
        if isinstance(value, tuple):
            ret = getattr(element, command)(*value)
        else:
            ret = getattr(element, command)(value)
        return ret

    def goto(self, url=None, url_args=None, force=False):
        """
        Navigates the browser.
        By default goes to the definition keyed by 'goto'.
        """
        url = url or self.definitions['goto']['value']
        if url_args:
            url = url % url_args

        # Get the current url so we can avoid the goto and delay if necessary.
        current_url_components = urlparse(self.driver.current_url)
        current_url = current_url_components.path
        if current_url_components.fragment:
            current_url += '#{}'.format(current_url_components.fragment)
        # Strip out double-slashes.
        current_url = current_url.replace('//', '/')
        if url == current_url and not force:
            print "can't goto({}), already there".format(url)
            return

        self.testcase.navigate_to(url)
        print 'goto(%s)' % url
        time.sleep(settings.GOTO_DELAY)

    def click(self, element, index=None):
        self.command('click', element, index=index)

    def hover(self, element, index=None):
        self.command('hover', element, index=index)

    def assert_(self, element, assertions=None, values=None, index=None, find_displayed=False):
        assertions = assertions or self.get_assertions(element)

        if index:
            print 'Assert %s[%s] : %s' % (element, index, assertions)
        else:
            print 'Assert %s : %s' % (element, assertions)

        self.get_element(element, index=index).assert_(assertions, values, find_displayed=find_displayed)

    @staticmethod
    def pause():
        try:
            input('press Enter to end script...')
        except:
            pass

    def input(self, element, value, index=None):
        self.command('input', element, value=value, index=index)

    def select_by_text(self, element, value, index=None):
        self.select(element, 'text', value, index=index)

    def select(self, element, select_by, value, index=None):
        self.command('select_by', element, (select_by, value, ), index=index)

    def assert_text(self, text):
        self.assert_('body', [a.CONTAINS], {a.CONTAINS: text})

    def assert_no_text(self, text):
        self.assert_('body', [a.NOT_CONTAINS], {a.NOT_CONTAINS: text})

    def capture(self, element, index=None, pattern=None, result_index=None, _property=None, _property_key=None):
        return self.get_element(element, index=index).capture(pattern=pattern,
                                                              result_index=result_index,
                                                              _property=_property,
                                                              _property_key=_property_key)

    def execute_script(self, value):
        print 'execute_script %s' % value
        self.driver.execute_script(value)

    def alert(self, value=None):
        value = value or r"^[\s\S]*$"
        self.testcase.assertRegexpMatches(self.testcase.close_alert_and_get_its_text(), value)

    def text(self, element, index=None):
        return self.command('text', element, index=index)

    def drag_drop(self, source, destination, source_index=None, destination_index=None):
        e1 = self.get_element(source, index=source_index)
        e2 = self.get_element(destination, index=destination_index)
        e1.drag_to(e2)