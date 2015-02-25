class TestScript:
    driver = None
    testcase = None

    def __init__(self, testcase):
        self.driver = testcase.driver
        self.testcase = testcase