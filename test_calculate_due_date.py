import unittest
from calculate_due_date import CalculateDueDate
from calculate_due_date import Days
from calculate_due_date import Seconds

class TestDueDateCalculator(unittest.TestCase):
    
    def test_attribute_validity(self):
        # Current GMT date/time at code creation (00:00:00 June 29, 2021 Tuesday)
        Tuesday = 1624924800 
        # Valid turnaround time
        Turnaround = 8 * Seconds.hour # 08:00 hours time
       
        # Just valid submit date/time
        TuesdayWorkStart = Tuesday + Seconds.workStart # 09:00:00
        Resolved = TuesdayWorkStart + Seconds.day
        self.assertEqual(CalculateDueDate(TuesdayWorkStart, Turnaround), Resolved)
         
        # Just invalid submit date/time raises outside of working hours exception
        BeforeWorkStart = TuesdayWorkStart - 1 # 08:59:59
        self.assertRaises(ValueError, CalculateDueDate, BeforeWorkStart, Turnaround)
        
        # Just invalid submit date/time raises outside of working hours exception
        AfterWorkEnd = Tuesday + Seconds.workEnd # 17:00:00
        self.assertRaises(ValueError, CalculateDueDate, AfterWorkEnd, Turnaround)
        
        # Just valid submit date/time
        TuesdayWorkEnd = AfterWorkEnd - 1 # 16:59:59
        Resolved = TuesdayWorkEnd + Seconds.day
        self.assertEqual(CalculateDueDate(TuesdayWorkEnd, Turnaround), Resolved)
        
        # Weekend submit date/time raises exception
        SundayWorkStart = TuesdayWorkStart + 5 * Seconds.day
        self.assertRaises(ValueError, CalculateDueDate, SundayWorkStart, Turnaround)
        
        # Negative turnaround raises exception
        self.assertRaises(ValueError, CalculateDueDate, TuesdayWorkStart, -1)
        
 
    def rolling_tests_for_a_week(self, submit, turnaround, resolved):
        """Generic testcase running for 7 days (7 tests in 1).
        Increases the initial submit date 24 hours per step.
        In each step the resolve date/time is updated to the correct value.
        Prints out current day of the week in case of failure.
        
        Args:
            submit: valid submission date/time (in Unix time format)
            turnaround: valid turnaround time (in seconds)
            resolved: the solution date/time to the initial submit-turnaround pair"""
        
        for n in range(Days.week):
            dayOfSubmit, _ = Seconds.dayTime(submit)
            with self.subTest(dayOfSubmit=dayOfSubmit):
                if Days.isWeekend(dayOfSubmit):
                    self.assertRaises(ValueError, CalculateDueDate, submit, turnaround)
                else:
                    self.assertEqual(CalculateDueDate(submit, turnaround), resolved)
            # Update counters
            submit += Seconds.day
            resolved += Seconds.day
            # Skip weekend for resolved date/time
            dayOfResolved, _ = Seconds.dayTime(resolved)
            if Days.isWeekend(dayOfResolved):
                resolved += Seconds.weekendLength
   
    def test_rolling_9_whole_days(self):
        # Initial submit 12:12:01 Aug 01, 1492 Monday, resolve at next Friday
        MondayWorkStart = -15065827200 + Seconds.workStart
        submit = MondayWorkStart + 2 * Seconds.hour + 4321
        turnaround = 9 * Seconds.workLength
        resolved = submit + 11 * Seconds.day
        # see description for self.rolling_tests_for_a_week above
        self.rolling_tests_for_a_week(submit, turnaround, resolved)
        
    def test_rolling_9_whole_days_plus_delta(self):
        # Initial submit 15:18:31 Sep 25, 2006 Monday, resolve at next Friday
        MondayWorkStart = 1159142400 + Seconds.workStart
        submit = MondayWorkStart + 6 * Seconds.hour + 1111
        delta = 47 * Seconds.min + 53
        turnaround = 9 * Seconds.workLength + delta
        resolved = submit + 11 * Seconds.day + delta
        # see description for self.rolling_tests_for_a_week above
        self.rolling_tests_for_a_week(submit, turnaround, resolved)

    def test_rolling_9_and_a_half_days_plus_delta(self):
        # Initial submit 13:00:00 June 27, 2366 Monday, resolve 2 weeks later
        MondayWorkStart = 12511843200 + Seconds.workStart
        halfday = 4 * Seconds.hour + 1234
        submit = MondayWorkStart + halfday
        delta = 49 * Seconds.min + 42
        turnaround = 10 * Seconds.workLength - halfday + delta
        resolved = MondayWorkStart + 2 * Seconds.week + delta
        # see description for self.rolling_tests_for_a_week above
        self.rolling_tests_for_a_week(submit, turnaround, resolved)

        
if __name__ == '__main__':
    unittest.main()