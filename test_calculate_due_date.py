import unittest
from calculate_due_date import CalculateDueDate
from calculate_due_date import Seconds

class TestDueDateCalculator(unittest.TestCase):
    
    def test_attribute_validity(self):
        # Current GMT date at code creation (00:00:00 June 29, 2021 Tuesday)
        # (see https://www.epochconverter.com/)
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
        TuesdayWorkEnd =  AfterWorkEnd - 1 # 16:59:59
        Resolved = TuesdayWorkEnd + Seconds.day
        self.assertEqual(CalculateDueDate(TuesdayWorkEnd, Turnaround), Resolved)
        
        # Weekend submit date/time raises exception
        SundayWorkStart = TuesdayWorkStart + 5 * Seconds.day
        self.assertRaises(ValueError, CalculateDueDate, SundayWorkStart, Turnaround)
        
        # Negative turnaround raises exception
        self.assertRaises(ValueError, CalculateDueDate, TuesdayWorkStart, -1)
        
        
    def test_stretching_accross_weeks_and_days(self):
        # Future GMT date/time (09:00:00 June 28, 2366 Tuesday)
        TuesdayWorkStart = 12511929600 + Seconds.workStart
        # Average submit date/time (13:00:00 June 29, 2021 Tuesday)
        TuesdayAverage = TuesdayWorkStart + Seconds.workLength // 2
       
        # Tuesday 13:00 to 2 weeks later Monday 13:00
        Turnaround = 9 * Seconds.workLength
        Resolved = TuesdayAverage + 2 * Seconds.week - Seconds.day
        self.assertEqual(CalculateDueDate(TuesdayAverage, Turnaround), Resolved)
       
        # Tuesday 13:00 to 2 weeks later Monday 13:47
        delta = 47 * Seconds.min
        Turnaround += delta
        Resolved += delta
        self.assertEqual(CalculateDueDate(TuesdayAverage, Turnaround), Resolved)
       
        # Tuesday 13:00 to 2 weeks later Tuesday 09:47
        Turnaround += Seconds.workLength - Seconds.workLength // 2
        Resolved = TuesdayWorkStart + 2 * Seconds.week + delta
        self.assertEqual(CalculateDueDate(TuesdayAverage, Turnaround), Resolved)

        
if __name__ == '__main__':
    unittest.main()