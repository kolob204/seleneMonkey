from selenium.webdriver.common.keys import Keys

from libs.browser import open_url
from libs.conditions import s


class AbstractPage(object):

    def perform_search(self, searching_str):
        self.input_search.send_keys(searching_str, Keys.ENTER)

    def check_first_search_result(self, condition, value):
        self.first_search_result.should(condition, value)

    def open_page(self):
        open_url(self.url)


class GooglePage(AbstractPage):

    def __init__(self):
        self.url = "http://google.com/ncr"
        # self.url = "http://yandex.ru"
        self.input_search = s("[name='q']")
        self.first_search_result = s(".g:nth-child(1)")


class Duckduckgo(AbstractPage):

    def __init__(self):
        self.url = "https://duckduckgo.com/"
        self.input_search = s("#search_form_input_homepage")
        self.first_search_result = s(".nrn-react-div:nth-child(1)")
