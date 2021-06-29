import unittest
from calculate_due_date import CalculateDueDate
from calculate_due_date import Seconds

class TestDueDateCalculator(unittest.TestCase):
    
    def test_attribute_validity(self):
        # Current GMT date at code creation from https://www.epochconverter.com/
        Tuesday = 1624924800 # 00:00:00 June 29, 2021 (Tuesday)
        # Valid turnaround time
        Turnaround = 8 * Seconds.hour # 08:00 hours time
       
        # Just valid submit date
        TuesdayWorkStart = Tuesday + Seconds.workStart # 09:00:00
        Resolved = TuesdayWorkStart + Seconds.day
        self.assertEqual(CalculateDueDate(TuesdayWorkStart, Turnaround), Resolved)
         
        # Just invalid submit date raises outside of working hours exception
        BeforeWorkStart = TuesdayWorkStart - 1 # 08:59:59
        self.assertRaises(ValueError, CalculateDueDate, BeforeWorkStart, Turnaround)
        
        # Just valid submit date
        TuesdayWorkEnd = Tuesday + Seconds.workEnd # 17:00:00
        Resolved = TuesdayWorkEnd + Seconds.day
        self.assertEqual(CalculateDueDate(TuesdayWorkEnd, Turnaround), Resolved)
        
        # Just invalid submit date raises outside of working hours exception
        AfterWorkEnd = TuesdayWorkEnd + 1 # 17:00:01
        self.assertRaises(ValueError, CalculateDueDate, AfterWorkEnd, Turnaround)
        
        # Weekend submit date raises exception
        SundayWorkStart = TuesdayWorkStart + 5 * Seconds.day
        self.assertRaises(ValueError, CalculateDueDate, SundayWorkStart, Turnaround)
        
        # Negative turnaround raises exception
        self.assertRaises(ValueError, CalculateDueDate, TuesdayWorkStart, -1)
        
if __name__ == '__main__':
    unittest.main()