from BaseTest import BaseTest
from Pages import GooglePage, Duckduckgo
from libs import browser
from libs.conditions import text, s

browser.add_browser_option('-start-maximized')


class Test(BaseTest):
    def __init__(self):
        g = GooglePage()
        g.open_page()
        g.perform_search("selenium")
        g.check_first_search_result(text, "Selenium automates browsers")
        g.first_search_result.find_element_by_css_selector(".g a").click()

        d = Duckduckgo()
        d.open_page()
        d.perform_search("selenium")
        d.check_first_search_result(text, "Selenium WebDriver. If you want to create robust")


Test()
