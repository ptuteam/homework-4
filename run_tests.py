# -*- coding: utf-8 -*-

import sys
import unittest

from tests.car_showrooms.add_showroom_test import AddShowroomFormTest
from tests.car_showrooms.list_showroom_test import ShowroomListTest
from tests.car_showrooms.list_special_offers_test import SpecialOffersListTest
from tests.car_showrooms.search_showroom_tests import *

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(IsOfficialCheckboxTest),
    ))
    result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        suite = unittest.TestSuite((
            unittest.makeSuite(ShowroomListTest),
        ))
        result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        suite = unittest.TestSuite((
            unittest.makeSuite(SpecialOffersListTest),
        ))
        result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        suite = unittest.TestSuite((
            unittest.makeSuite(AddShowroomFormTest),
        ))
        result = unittest.TextTestRunner().run(suite)

    sys.exit(not result.wasSuccessful())
