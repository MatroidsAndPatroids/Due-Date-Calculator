# Due Date Calculator :stopwatch:

##### Rules ('technical' specification)
- Input: Takes the submit date/time and turnaround time.
- Output: Returns the date/time when the issue is resolved.<br/><br/>
- Working hours are from 9AM to 5PM on every working day, Monday to Friday.
- Holidays should be ignored (e.g. A holiday on a Thursday is considered as a
working day. A working Saturday counts as a non-working day.).
- The turnaround time is defined in working hours (e.g. 2 days equal 16 hours).
If a problem was reported at 2:12PM on Tuesday and the turnaround time is
16 hours, then it is due by 2:12PM on Thursday.
- A problem can only be reported during working hours. (e.g. All submit date
values are set between 9AM to 5PM.)
- Do not use any third-party libraries for date/time calculations (e.g. Moment.js,
Carbon, Joda, etc.) or hidden functionalities of the built-in methods.

##### Developer notes
- The input and output format was not specified (to be asked for?), therefore I've chosen a simple solution. Creating a fully fledged 'Time class' made no sense as of yet, human friendly interface was not required
- It is generally a bad practice to use global variables. If no further changes are required, they should be forced to remain constants

##### Contents
- _calculate_due_date.py_  contains the required CalculateDueDate method with helper classes and documentation
- _test_calculate_due_date.py_  contains unit tests for the above and can be executed as such
- _README.md_  - this file