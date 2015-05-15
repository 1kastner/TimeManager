__author__ = 'carolinux'


import TimeManager.time_util as time_util
import TimeManager.bcdate_util as bcdate_util
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import unittest


__author__="Karolina Alexiou"
__email__="karolina.alexiou@teralytics.ch"

class TestBCDates(unittest.TestCase):

    bc_dates = ["0020 BC", "0200 BC", "1999 BC", "0200 AD"]

    @classmethod
    def setUpClass(cls):
        time_util.setCurrentMode(time_util.ARCHAELOGY_MODE)

    @classmethod
    def tearDownClass(cls):
        time_util.setCurrentMode(time_util.NORMAL_MODE)

    def test_is_mode_set(self):
        assert(time_util.is_archaelogical())

    def test_bc_date_additions(self):
        for datestr in self.bc_dates:
            dt = time_util.str_to_datetime(datestr)
            new_date = dt + relativedelta(years=1)
            assert(new_date.y == dt.y+1)

    def test_ad(self):
        val ="0001 AD"
        dt = time_util.timeval_to_datetime(val)
        assert(dt == bcdate_util.BCDate(1))

    def test_bc_date_conversions_str(self):
        for datestr in self.bc_dates:
            dt = time_util.str_to_datetime(datestr)
            datestr2 = time_util.datetime_to_str(dt)
            assert(datestr==datestr2)

    def test_bc_date_conversions_epoch(self):
        for datestr in self.bc_dates:
            print datestr
            dt = time_util.str_to_datetime(datestr)
            epoch = time_util.datetime_to_epoch(dt)
            dt2 = time_util.epoch_to_datetime(epoch)
            assert(dt==dt2)

    def test_date_with_bc_is_detected_as_such(self):
        dtstr="0020 BC"
        assert(time_util.get_format_of_timeval(dtstr) == bcdate_util.BC_FORMAT)
        assert(time_util.timeval_to_datetime(dtstr,bcdate_util.BC_FORMAT) == bcdate_util.BCDate(-20,1,1))
        dtstr="0020 AD"
        assert(time_util.get_format_of_timeval(dtstr) == bcdate_util.BC_FORMAT)
        assert(time_util.timeval_to_datetime(dtstr,bcdate_util.BC_FORMAT) == bcdate_util.BCDate(20,1,1))
        assert(time_util.DateTypes.determine_type(dtstr) == time_util.DateTypes.DatesAsStringsArchaelogical)
