from selenium import webdriver

BASE_URL = "https://github.com/"

# How long to wait for commands.
IMPLICITLY_WAIT = 4

# For negative assertions, set the delay much lower.
IMPLICITLY_WAIT_QUICK_ASSERT = 1

# Add a delay after page navigation.
GOTO_DELAY = 0.5

# Add a delay between commands.
PER_COMMAND_DELAY = 0.1

# Configure the browser to use.
DRIVER = webdriver.Firefox
