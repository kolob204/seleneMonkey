import time
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from libs.browser import get_driver

POLL_FREQUENCY = 0.5
IGNORED_EXCEPTIONS = (NoSuchElementException,)  # exceptions ignored during calls to the method


class waiter(object):
    def __init__(self, driver, timeout, ignored_exceptions=None):
        self._timeout = timeout
        self._driver = driver
        self._ignored_exceptions = None

        exceptions = list(IGNORED_EXCEPTIONS)
        if ignored_exceptions is not None:
            try:
                exceptions.extend(iter(ignored_exceptions))
            except TypeError:  # ignored_exceptions is not iterable
                exceptions.append(ignored_exceptions)
        self._ignored_exceptions = tuple(exceptions)

    def until(self, method, message=''):
        screen = None
        stacktrace = None

        end_time = time.time() + self._timeout
        while True:
            try:
                value = method()
                if value:
                    return value
            except self._ignored_exceptions as exc:
                screen = getattr(exc, 'screen', None)
                stacktrace = getattr(exc, 'stacktrace', None)
            time.sleep(POLL_FREQUENCY)
            if time.time() > end_time:
                break
        raise TimeoutException(message, screen, stacktrace)

class WaitingElement():
    def __init__(self, css_locator):
        self._locator = css_locator

    def _finder(self):
        return get_driver().find_element_by_css_selector(self._locator)

    # Lazy Proxy (re-find element)
    def __getattr__(self, item):
        return getattr(waiter(get_driver(), 4).until(visibile(self._finder)), item)

    def should(self, condition, *args):
        WebDriverWait(get_driver(), 4).until(condition(self._finder, *args))
        return self

# Переопределение Selenium conditions
# Копии классов из ec.text_to_be_present_in_element
# Переделанные под свой вариант
class text(object):
    def __init__(self, finder, text_):
        self.finder = finder
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = self.finder().text
            return self.text in element_text
        except StaleElementReferenceException:
            return False


class visibile(object):
    def __init__(self, finder):
        self.finder = finder

    def __call__(self):
        try:
            if self.finder().is_displayed():
                return self.finder()
        except StaleElementReferenceException:
            return None


class clickable(object):
    def __init__(self, finder):
        self.finder = finder

    def __call__(self, driver):
        try:
            element = self.finder()
            return element.is_displayed() and element.is_enabled
        except StaleElementReferenceException:
            return False


def s(css_selector):
    return WaitingElement(css_selector)