'''
The current time format is Unix time stored as integer.
Eg. time 0 = January 1, 1970 (Thursday) 00:00 in the morning

Seconds class contains global constants used by the CalculateDueDate method.
Requirements for a time format (input/output) should be specified (asked for)!
This could result upgrading this into a Time class, substituting it
with an appropriate module, or replacing it altogether.
'''
class Seconds:
    # International constants
    min = 60
    hour = 60 * min
    day = 24 * hour
    week = 7 * day
    # 'day 0' is January 1, 1970 (Thursday), see: Unix time
    weekendStart = 2 * day # Saturday morning 12:00AM
    weekendEnd = 4 * day # Monday morning 12:00AM
   
    # Working hour boundaries
    workStart = 9 * hour
    workEnd = 17 * hour
    
    # Seconds passed since last Monday morning 12:00AM
    def weekTime(datetime):
        return datetime % Seconds.week
    
    # Seconds passed since current morning 12:00AM
    def dayTime(datetime):
        return datetime % Seconds.day


'''
CalculateDueDate method

Usage example: CalculateDueDate(1095379198, 16 * const.SEC_PER_HOUR)
'''
def CalculateDueDate(submit_date, turnaround_time):
    if turnaround_time < 0:
        raise ValueError('Negative turnaround time')
    
    weekTime = Seconds.weekTime(submit_date)
    #print(f'{weekTime = }, {weekTime // Seconds.day = }')
    if Seconds.weekendStart <= weekTime < Seconds.weekendEnd:
        raise ValueError('Submit date/time on weekend')
    
    dayTime = Seconds.dayTime(weekTime)
    #print(f'{dayTime = }, {dayTime / Seconds.hour = }')
    if not Seconds.workStart <= dayTime <= Seconds.workEnd:
        raise ValueError('Submit date/time outside of working hours')
    
    return -1

