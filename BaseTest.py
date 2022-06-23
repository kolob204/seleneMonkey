from libs.browser import close_driver


class BaseTest:
    def __del__(self):
        close_driver()
