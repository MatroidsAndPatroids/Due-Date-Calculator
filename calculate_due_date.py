"""Calculate Due Date

Time format is Unix time stored as integer 
(eg. time 0 = January 1, 1970 Thursday 00:00:00 in the morning)
Days of week are: 0 = Thursday, 1 = Friday, ..., 6 = Wednesday
Integer dates can be manipulated (shifted) by simple integer addition/subtraction.
The Days and Seconds classes provide some useful constants for this.

There was no need to consider leap years, day-light saving time or time zones
"""


class Days:
    """Global constants and methods for days of the week"""
    
    # International constants
    week = 7
    weekendStart = 2 # Saturday, inclusive
    weekendEnd = 4 # Monday, exclusive
    weekendLength = weekendEnd - weekendStart
    workLength = week - weekendLength
    
    # True, if dayOfWeek = 0, 1, ..., 6 is marked as weekend
    def isWeekend(dayOfWeek):
        return Days.weekendStart <= dayOfWeek < Days.weekendEnd


class Seconds:
    """Global constants and methods for seconds of the day"""

   # International constants
    min = 60
    hour = 60 * min
    day = 24 * hour
    week = 7 * day
   
    # Working hour boundaries
    workStart = 9 * hour # 9AM, inclusive
    workEnd = 17 * hour # 17AM, exclusive
    workLength = workEnd - workStart
    
    # Current day of the week and the seconds passed since current morning 00:00
    def dayTime(datetime):
        weekSeconds = datetime % Seconds.week
        dayOfWeek, timeOfDay = divmod(weekSeconds, Seconds.day)
        return dayOfWeek, timeOfDay
    
    # True, if 0 <= timeOfDay < 86400 is during the working hours
    def isWorkingHour(timeOfDay):
        return Seconds.workStart <= timeOfDay < Seconds.workEnd


def CalculateDueDate(submit_datetime, turnaround_time):
    """Due date calculator for an issue tracking system
    
    Args:
        submit_datetime: issue submission date/time (in Unix time format)
        turnaround_time: worktime required to resolve the issue (in seconds)
    
    Returns:
        Resolve date/time of an issue
    
    Example:
        CalculateDueDate(1159277160, 16 * Seconds.hour)
        (1159277160 = September 26, 2006 Tuesday 13:26:00,
        see https://www.epochconverter.com/)"""
    
    # Validate arguments    
    if turnaround_time < 0:
        raise ValueError('Negative turnaround time')
    
    dayOfWeek, timeOfDay = Seconds.dayTime(submit_datetime) 
    if Days.isWeekend(dayOfWeek):
        raise ValueError('Submit date/time on weekend')

    if not Seconds.isWorkingHour(timeOfDay):
        raise ValueError('Submit date/time outside of working hours')
    
    # Shift submit date/time to Monday and adjust turnaround time accordingly
    delta = (dayOfWeek - Days.weekendEnd) % Days.week
    submit_datetime -= delta * Seconds.day
    turnaround_time += delta * Seconds.workLength
    
    # Shift submit date/time to 9AM and adjust turnaround time accordingly
    delta = timeOfDay - Seconds.workStart
    submit_datetime -= delta
    turnaround_time += delta
    
    # Split turnaround time into workweeks + workdays + seconds
    turnaroundDays, turnaroundSeconds = divmod(turnaround_time, Seconds.workLength)
    turnaroundWeeks, turnaroundDays = divmod(turnaroundDays, Days.workLength)
    
    # Assemble resolve date/time
    resolve_datetime = submit_datetime + turnaroundWeeks * Seconds.week
    resolve_datetime += turnaroundDays * Seconds.day
    resolve_datetime += turnaroundSeconds
    return resolve_datetime

