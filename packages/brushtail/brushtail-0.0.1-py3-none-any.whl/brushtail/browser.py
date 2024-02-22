# builtin
import time
import os
from enum import Enum
from dataclasses import dataclass
from typing import Any, List

# external
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DriverType(Enum):
    Requests = 1            # Requests is used for the web component, beautifulsoup for parsing the results
    SeleniumChrome = 2      # Selenium uses Chrome to navigate comprehensively
    SeleniumFirefox = 4     # Selenium uses Firefox to navigate comprehensively


class SelectionStyle(Enum):
    Empty = 1               # Nothing is focused
    Single = 2              # Single focus
    Multiple = 3            # Multiple focus


@dataclass
class HistoryItem:
    selection: SelectionStyle
    items: Any


class Browser:
    """
    A simple system to make webscraping scripts more clear.
    Functions can be chained for effect (like in tools such as ffmpeg) where the root browser object is mutated and returned each time.
    The browser object retains "focus" on the target element(s). Subsequently you can get info about said element.
    """
    driver_type = DriverType.Requests

    # todo make working with requests more aligned with the driver system? maybe it's not worth it
    requests_content = ''
    requests_response = ''

    # Selenium driver reference needs to be held
    driver_seleniumchrome = None
    driver_seleniumfirefox = None

    single_focus = True
    focused_element = None
    focused_elements = None
    history: List[HistoryItem] = []

    def __init__(self, driver_type: DriverType):
        self.driver_type = driver_type
        match driver_type:
            case DriverType.Requests:
                # no initialization required here
                pass

            case DriverType.SeleniumChrome:
                # todo pass in configuration
                options = ChromeOptions()
                # todo implement this in non-deprecated form
                # options.headless = True
                self.driver_seleniumchrome = webdriver.Chrome(options=options)

            case DriverType.SeleniumFirefox:
                # todo pass in configuration
                options = FirefoxOptions()
                # todo implement this in non-deprecated form
                # options.headless = True
                self.driver_seleniumfirefox = webdriver.Firefox(options=options)

    @staticmethod
    def with_requests():
        return Browser(DriverType.Requests)

    @staticmethod
    def with_selenium_chrome():
        return Browser(DriverType.SeleniumChrome)

    @staticmethod
    def with_selenium_firefox():
        return Browser(DriverType.SeleniumFirefox)

    # INIT

    def load(self, uri):
        print(f"Loading {uri}")

        # Always clear focus history on page load
        self.history = []
        self.clear_focus()

        # Handle driver specifics
        match self.driver_type:
            case DriverType.Requests:
                pass
                raise NotImplementedError("DriverType.Requests is not implemented.")

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                self._selenium_root().get(uri)

        return self

    # FOCUS INTERNAL

    def _set_focus(self, target, single_focus):
        if target is None or target is []:
            return

        if single_focus:
            self.focused_elements = None
            self.focused_element = target
            self.single_focus = True

            self.history.append(HistoryItem(selection=SelectionStyle.Single, items=target,))
        else:
            self.focused_elements = target
            self.focused_element = None
            self.single_focus = False

            self.history.append(HistoryItem(selection=SelectionStyle.Multiple, items=target, ))

    def _get_element_single(self, starting_point, element=None, _class=None, _id=None):
        result = None
        try:
            if _class is not None:
                result = starting_point.find_element(By.CLASS_NAME, _class)
            elif element is not None:
                result = starting_point.find_element(By.TAG_NAME, element)
            elif _id is not None:
                result = starting_point.find_element(By.ID, _id)
        except NoSuchElementException:
            pass

        return result

    def _get_element_multiple(self, starting_point, element=None, _class=None, _id=None):
        results = None
        try:
            if _class is not None:
                results = starting_point.find_elements(By.CLASS_NAME, _class)
            elif element is not None:
                results = starting_point.find_elements(By.TAG_NAME, element)
            elif _id is not None:
                results = starting_point.find_elements(By.ID, _id)
        except NoSuchElementException:
            pass

        return results

    def _selenium_root(self):
        match self.driver_type:
            case DriverType.SeleniumChrome:
                return self.driver_seleniumchrome

            case DriverType.SeleniumFirefox:
                return self.driver_seleniumfirefox

    # NAVIGATION
    def clear_focus(self):
        """
        Clear the focus without reloading anything
        """
        self.single_focus = True
        self.focused_element = None
        self.focused_elements = None

        self.history.append(HistoryItem(selection=SelectionStyle.Empty, items=None,))

        return self

    def back(self, index=2):
        """
        Refocus a previously focused set of elements.
        """
        target = self.history[-index]

        single_focus = True
        if target.selection == SelectionStyle.Multiple:
            single_focus = False

        self._set_focus(target.items, single_focus=single_focus)

        return self

    def inside(self, element=None, _class=None, _id=None, foreach=True):
        """
        Focus on a target element.
        Equivalent to find

        The foreach element means that if there is multiple focus, then each focussed element returns one item per find.
        Setting foreach to false means that only one item will be returned overall.
        """
        if element is not None:
            print(f"Looking inside element {element}")
        elif _class is not None:
            print(f"Looking inside class {_class}")
        elif _id is not None:
            print(f"Looking inside id {_id}")

        match self.driver_type:
            case DriverType.Requests:
                # use bs4 to parse content
                pass

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                """
                todo should this start from an inside_all?
                    the issue is that inside should result in 1 focussed element 
                    but you could have other focussed elements and be looking for 1 element inside that 
                    let's just skip this case for now, but I think perhaps we need to change it so that 
                        focused_element = focused_elements[0]
                    and whenever we call inside or inside_all we check all elements 
                    actually this makes sense because then inside is always just 
                        focussed_elements = x.find_elements(x, y)

                    the trick is that to get links text etc from children you need to be explicit 
                        perhaps include options to get links recursively? get outertext vs inner? 

                """
                starting_point = self._selenium_root()
                if self.single_focus:
                    if self.focused_element is not None:
                        starting_point = self.focused_element

                    result = self._get_element_single(starting_point, element, _class, _id)
                    self._set_focus(result, single_focus=True)

                elif self.focused_elements is not None:
                    starting_points = self.focused_elements

                    results = []
                    for p in starting_points:
                        result = self._get_element_single(p, element, _class, _id)
                        if result is not None:
                            results.append(result)

                        if not foreach and len(results) > 0:
                            self._set_focus(results[0], single_focus=True)
                            results = []  # empty results so following checks don't grab it
                            break

                    if results:
                        self._set_focus(results, single_focus=False)

                # todo implement with wait
                # wait = WebDriverWait(self.driver_seleniumchrome, 10)
                # # todo use the given keyword arg
                # self.focused_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, _class)))

        return self

    def inside_all(self, element=None, _class=None, _id=None, foreach=True):
        """
        Focus on a target element.
        Equivalent to find_all
        """
        if element is not None:
            print(f"Looking inside element {element}")
        elif _class is not None:
            print(f"Looking inside class {_class}")
        elif _id is not None:
            print(f"Looking inside id {_id}")

        match self.driver_type:
            case DriverType.Requests:
                # use bs4 to parse content
                pass

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                starting_point = self.driver_seleniumchrome

                if self.single_focus:
                    if self.focused_element is not None:
                        starting_point = self.focused_element

                    results = self._get_element_multiple(starting_point, element, _class, _id)
                    if results is not None:
                        self._set_focus(results, single_focus=False)

                elif self.focused_elements is not None:
                    starting_points = self.focused_elements

                    results = []

                    for p in starting_points:
                        result = self._get_element_multiple(p, element, _class, _id)
                        if result is not None:
                            results.append(result)

                    self._set_focus(results, single_focus=False)

        print(self.focused_elements)
        return self

    def wait(self, seconds):
        """
        Wait time in seconds, using naive time.sleep method.
        It's not maximally efficient, but neither is life.
        """
        time.sleep(seconds)
        return self

    def click(self, foreach=False):
        """
        Click on the focused element
        TODO implement foreach
        """
        match self.driver_type:
            case DriverType.Requests:
                raise NotImplementedError("DriverType.Requests does not have a click function.")

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                if self.focused_element is None:
                    return

                self.focused_element.click()

        return self

    def scroll_to_bottom(self, delay=0.5):
        """

        :param delay: the time to pause between scroll attempts
        """
        match self.driver_type:
            case DriverType.Requests:
                raise NotImplementedError("DriverType.Requests does not have a scroll function.")

            case DriverType.SeleniumFirefox:
                raise NotImplementedError("DriverType.SeleniumFirefox scroll function is not implemented.")

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                # Get scroll height
                last_height = self.driver_seleniumchrome.execute_script("return document.body.scrollHeight")

                while True:
                    # Scroll down to bottom
                    self.driver_seleniumchrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                    # Wait to load page
                    time.sleep(delay)

                    # Calculate new scroll height and compare with last scroll height
                    new_height = self.driver_seleniumchrome.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

        return self

    # CONTENT
    # These functions are to do with saving out content - screenshots, html page, etc

    def screenshot(self, screenshot_path):
        """
        Screenshot the focussed elements
        """
        match self.driver_type:
            case DriverType.Requests:
                raise NotImplementedError("DriverType.Requests does not have a screenshot function.")

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                if self.focused_element is not None:
                    self.focused_element.screenshot(screenshot_path)

                if self.focused_elements:
                    for i, e in enumerate(self.focused_elements):
                        path_chunks = screenshot_path.split(".")
                        # todo make this path logic less error prone
                        numbered_path = f"{path_chunks[0]}_{i}.{path_chunks[-1]}"
                        e.screenshot(numbered_path)

        return self

    def save(self, path, name=None):
        """
        Save the page content
        """
        match self.driver_type:
            case DriverType.Requests:
                raise NotImplementedError("DriverType.Requests does not have a screenshot function.")

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                out_name = self.driver_seleniumchrome.current_url.split('/')[-1]
                if name is not None:
                    out_name = name
                out_path = os.path.join(path, out_name)

                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(self.driver_seleniumchrome.page_source)

        return self

    @staticmethod
    def download(url, path):
        """
        Download a webpages content
        TODO return success
        """
        with open(path, 'wb') as f:
            r = requests.get(url)
            f.write(r.content)

    # GET FUNCTIONS
    # all the get functions directly return some data, whereas the other methods act as chainable controls
    # Get all links/src/html should be the default - irrespective of the focus selection - so it's idiot proof

    def get_title(self) -> str:
        match self.driver_type:
            case DriverType.Requests:
                # use bs4 to parse content
                pass

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                return self._selenium_root().title

    def get_links(self, _class=None, element=None):
        """
        Get all contained links, provided their parent matches the given constraints.
        """
        match self.driver_type:
            case DriverType.Requests:
                # use bs4 to parse content
                pass

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                links = []

                if self.single_focus:
                    if self.focused_element.get_attribute('href') is None:
                        return []
                    links.append(self.focused_element.get_attribute('href'))
                else:
                    for e in self.focused_elements:
                        if e.get_attribute('href') is None:
                            continue
                        links.append(e.get_attribute('href'))

                return links

    def get_srcs(self, _class=None, element=None):
        """
        Get all contained links, provided their parent matches the given constraints.
        Requires that you focus on a list of elements, rather than just one.
        """
        match self.driver_type:
            case DriverType.Requests:
                # use bs4 to parse content
                pass

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                links = []
                if self.single_focus:
                    if self.focused_element.get_attribute('src') is None:
                        return []
                    links.append(self.focused_element.get_attribute('src'))
                else:
                    for e in self.focused_elements:
                        if e.get_attribute('src') is None:
                            continue
                        links.append(e.get_attribute('src'))
                return links

    def get_text(self, _class=None, element=None):
        """
        Get all contained text, provided their parent matches the given constraints
        """
        match self.driver_type:
            case DriverType.Requests:
                # use bs4 to parse content
                pass

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                if self.single_focus:
                    return [self.focused_element.text, ]
                else:
                    results = []
                    for e in self.focused_elements:
                        if e.text is None:
                            continue
                        results.append(e.text)
                    return results

    def get_html(self, _class=None, element=None):
        """
        Get all contained text, provided their parent matches the given constraints
        """
        match self.driver_type:
            case DriverType.Requests:
                # TODO use bs4 to parse content
                raise NotImplementedError("DriverType.SeleniumFirefox is not implemented.")

            case DriverType.SeleniumChrome | DriverType.SeleniumFirefox:
                # if self.focused_element is None:
                #     raise Exception("No focused element to get.")
                # return self.focused_element.get_attribute("outerHTML")
                links = []
                if self.single_focus:
                    if self.focused_element.get_attribute('outerHTML') is None:
                        return []
                    links.append(self.focused_element.get_attribute('outerHTML'))
                else:
                    for e in self.focused_elements:
                        if e.get_attribute('outerHTML') is None:
                            continue
                        links.append(e.get_attribute('outerHTML'))
                return links
