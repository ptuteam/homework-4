# coding=utf-8
import os
import unittest
import urlparse

from selenium.webdriver import DesiredCapabilities, Remote
from selenium.webdriver.support.ui import WebDriverWait


class ShowroomPage(object):
    BASE_URL = 'https://cars.mail.ru/dealers/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class RegionSelectionForm(Component):
    COUNTRY = '//span[text()="{}"]'
    REGION = '//input[@class="input__data__value"]'
    SUBMIT_REGION = 'div.input__data__value.js-field_item'
    SUBMIT = '//span[text()="Выбрать"]'
    SELECT_BUTTON = 'span.js-geo_name'

    def open_form(self):
        self.driver.find_element_by_xpath(self.SELECT_BUTTON).click()

    def set_country(self, country):
        self.driver.find_element_by_xpath(self.COUNTRY.format(country)).click()

    def set_region(self, region):
        self.driver.find_element_by_xpath(self.REGION).send_keys(region)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_REGION).click()
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class FilterForm(Component):
    MODEL = '//input[@class="input__data__value"]'


class ExampleTest(unittest.TestCase):
    USERNAME = u'Дмитрий Котегов'
    USEREMAIL = 'kotegov_dima@mail.ru'
    PASSWORD = os.environ['TTHA2PASSWORD']
    BLOG = 'Флудилка'
    TITLE = u'ЗаГоЛоВоК'
    MAIN_TEXT = u'Текст под катом! Отображается внутри топика!'

    def setUp(self):
        browser = os.environ.get('TTHA2BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        auth_form = auth_page.form
        auth_form.open_form()
        auth_form.set_login(self.USEREMAIL)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

        user_name = auth_page.top_menu.get_username()
        self.assertEqual(self.USERNAME, user_name)

        create_page = CreatePage(self.driver)
        create_page.open()

        create_form = create_page.form
        create_form.blog_select_open()
        create_form.blog_select_set_option(self.BLOG)
        create_form.set_title(self.TITLE)
        create_form.set_main_text(self.MAIN_TEXT)
        create_form.submit()

        topic_page = TopicPage(self.driver)
        topic_title = topic_page.topic.get_title()
        topic_text = topic_page.topic.get_text()
        self.assertEqual(self.TITLE, topic_title)
        self.assertEqual(self.MAIN_TEXT, topic_text)

        topic_page.topic.open_blog()
        blog_page = BlogPage(self.driver)
        topic_title = blog_page.topic.get_title()
        topic_text = blog_page.topic.get_text()
        self.assertEqual(self.TITLE, topic_title)
        self.assertEqual(self.MAIN_TEXT, topic_text)

        blog_page.topic.delete()
        topic_title = blog_page.topic.get_title()
        topic_text = blog_page.topic.get_text()
        self.assertNotEqual(self.TITLE, topic_title)
        self.assertNotEqual(self.MAIN_TEXT, topic_text)