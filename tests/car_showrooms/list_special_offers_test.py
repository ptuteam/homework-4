import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from tests.car_showrooms.pages import ShowroomPage


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class SpecialOffersList(Component):
    __ITEM_TITLE = 'span.offer-mini__title'
    __ITEM_PAGE_TITLE = 'h1.car__title__text'
    # __ITEM_ADDRESS = 'div.dealer-card__adress'
    # __ITEM_PHONE = 'div.dealer-card__phone'
    # __PAGINATOR_CURRENT_PARAM = "a.pager__pin.pager__pin_perpage.pager__pin_on"
    # __PAGINATOR_PARAM = "a.pager__pin.pager__pin_perpage"

    def get_item_titles(self):
        item_titles = []
        item_pages_title = []
        for i in range(0, 3):
            if i == 0:
                item = self.driver.find_elements_by_css_selector(self.__ITEM_TITLE)[0]
            elif i == 1:
                item = self.driver.find_elements_by_css_selector(self.__ITEM_TITLE)[self.get_items_count()/2]
            elif i == 2:
                item = self.driver.find_elements_by_css_selector(self.__ITEM_TITLE)[self.get_items_count() - 1]

            item_titles.append(item.text)
            item.click()
            item_pages_title.append(self.get_item_page_title())
            self.driver.back()

        return item_titles, item_pages_title

    def get_item_page_title(self):
        return self.driver.find_element_by_css_selector(self.__ITEM_PAGE_TITLE).text
    #
    # def get_items_addresses(self):
    #     addresses = []
    #     for address in self.driver.find_elements_by_css_selector(self.__ITEM_ADDRESS):
    #         addresses.append(address.text)
    #     return addresses
    #
    # def get_items_phones(self):
    #     phones = []
    #     for phone in self.driver.find_elements_by_css_selector(self.__ITEM_PHONE):
    #         phones.append(phone.text)
    #     return phones

    def get_items_count(self):
        return len(self.driver.find_elements_by_css_selector(self.__ITEM_TITLE))

    # def set_pagination_count_params(self, count):
    #     for param in self.driver.find_elements_by_css_selector(self.__PAGINATOR_PARAM):
    #         if int(param.text) == count:
    #             param.click()
    #             return
    #
    # def get_pagination_count_current_param(self):
    #     return int(self.driver.find_element_by_css_selector(self.__PAGINATOR_CURRENT_PARAM).text)


class SpecialOffersListTest(unittest.TestCase):
    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test_redirect(self):
        page = ShowroomPage(self.driver)
        page.open()

        special_offers_list = page.special_offers_list
        item_titles, item_page_title = special_offers_list.get_item_titles()
        for i in range(0, len(item_titles)):
            self.assertTrue(item_page_title[i].startswith(item_titles[i]))

    # def test_short_info(self):
    #     page = ShowroomPage(self.driver)
    #     page.open()
    #
    #     special_offers_list = page.special_offers_list
    #
    #     addresses = special_offers_list.get_items_addresses()
    #     phones = special_offers_list.get_items_phones()
    #     for i in range(0, 5):
    #         if i == 0:
    #             index = 0
    #         elif i == 1:
    #             index = special_offers_list.get_items_count()/2 - 4
    #         elif i == 2:
    #             index = special_offers_list.get_items_count()/2
    #         elif i == 3:
    #             index = special_offers_list.get_items_count()/2 + 4
    #         elif i == 4:
    #             index = special_offers_list.get_items_count() - 1
    #
    #         address = addresses[index]
    #         self.assertIsNotNone(address)
    #
    #         phone = phones[index]
    #         self.assertIsNotNone(phone)
    #
    # def test_pagination(self):
    #     page = ShowroomPage(self.driver)
    #     page.open()
    #
    #     special_offers_list = page.special_offers_list
    #     self.assertEqual(special_offers_list.get_items_count(), special_offers_list.get_pagination_count_current_param())
    #     count_param = 40
    #     special_offers_list.set_pagination_count_params(count_param)
    #     self.assertEqual(special_offers_list.get_items_count(), count_param)
    #     count_param = 100
    #     special_offers_list.set_pagination_count_params(count_param)
    #     self.assertEqual(special_offers_list.get_items_count(), count_param)
