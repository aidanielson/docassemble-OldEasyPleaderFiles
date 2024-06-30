from datetime import date as dt, timedelta as td
from workalendar.usa import California
cal = California()
today_datetime = dt.today()
five_calendar_days = td(days=5)
two_calendar_days = td(days=2)
sixteen_court_days_from_today_datetime = cal.add_working_days(today_datetime, 16)
sixteen_court_days_from_today_string = sixteen_court_days_from_today_datetime.strftime('%A, %B %d, %Y')
eighteen_court_days_from_today_datetime = cal.add_working_days(today_datetime, 18)
eighteen_court_days_from_today_string = eighteen_court_days_from_today_datetime.strftime('%A, %B %d, %Y')
earliest_mail_service_date_datetime = sixteen_court_days_from_today_datetime + five_calendar_days
earliest_mail_service_date_string = earliest_mail_service_date_datetime.strftime('%A, %B %d, %Y')
earliest_overnight_or_fax_service_date_datetime = sixteen_court_days_from_today_datetime + two_calendar_days
earliest_overnight_or_fax_service_date_string = earliest_overnight_or_fax_service_date_datetime.strftime('%A, %B %d, %Y')