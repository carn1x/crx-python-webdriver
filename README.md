# crx-python-webdriver

Selenium WebDriver framework providing a boilerplate and encouraged design pattern to run on top of the WebDriver python bindings.

## Installation

### Python package installation

Install `crx-python-webdriver` using the following pip command.

`$ pip install git+https://github.com/carn1x/crx-python-webdriver.git`

 The package `selenium` will also be installed as a dependency (see https://pypi.python.org/pypi/selenium).

You will also need a compatible web browser with installed Selenium extension.

## Configuration

Your project settings should be defined at `conf.settings`. An example of this configuration file is available in at
`examples/conf/settings.py`.

By default it is set to use the Firefox driver which is installed as part of the Selenium pip package. Other browsers
may be supported as well however the drivers for these must be downloaded separately.

## Design Pattern

### Page Definitions
The concept of this boilerplate is to reduce the amount of repeated code by building a dictionary of page elements and
actions in relation to pages. These pages can inherit dictionaries from each other so for instance a BasePage may be
defined which holds the header and footer common to all pages and then a HomePage may subclass BasePage, adding its
own definitions whilst retaining the BasePage definitions.

Examples of this inheritance can be seen in `example/pages/`

These pages primarily define the dictionary of the page elements, however can also be useful to define shortcut methods
here. A most basic example would be a click method:

    def click_logo(self):
        self.click('logo')

Then when interacting with an instance of this Page, we can start typing `page.click_logo()` and we will get code
completion suggestions from our IDE.

Further than this however we can write more complex methods, such as:

    def signin(self, username, password):
        self.input('username', username)
        self.input('password', password)
        self.click('login')

With a wide array of test cases comes a ton of repetition, and so with well defined page definitions the amount of
repeated work is reduced.

### Test Scripts

A test script itself (examples in `example/scripts`) is mainly just a place to define individual test cases and group
them by some arbitrary functionality. The most obvious grouping is by page, but really there's no requirement.

Within these scripts we instantiate a Page and pass self as a parameter as this provides reference to useful properties:

    h = HomePage(self)
    h.goto()

### Primary Script

The primary script inherits `BaseTestCase` which itself is a subclass of python's `unittest.TestCase`. An example of
the primary script is at `example/main.py`

Like `TestCase`, any methods named beginning `test*` will execute upon `unittest.main()`

Additionally, `setUp()` allows us to run code before each test, for instance ensuring the database is reset back to an
expected state.


## Further Development

This boilerplate is far from a complete representation of what Selenium WebDriver offers however from an expansion
perspective I'll only be updating it myself as I encounter bugs for more aspects of WebDriver are required within my own
projects.

I will however be working to update the documentation as there's a lot more to this that the examples and this readme
currently convey.

Any commits, pull requests are more than welcome, and if you have feature requests or suggestions please post an issue
and if they aren't too mind boggling or I can produce a test case for them easily then I'll do my best to accommodate.