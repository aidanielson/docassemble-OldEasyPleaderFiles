__all__ = ['deadline_calculator_v7']

from datetime import date, timedelta
from typing import Union, Dict

# Complete California holidays dictionary through CY 2025
CA_HOLIDAYS_DICT = {
    date(2023, 1, 2): "New Year's Day",
    date(2023, 1, 16): "Martin Luther King, Jr. Birthday",
    date(2023, 2, 13): "Lincoln Day",
    date(2023, 2, 20): "Presidents' Day",
    date(2023, 3, 31): "Cesar Chavez Day",
    date(2023, 5, 29): "Memorial Day",
    date(2023, 6, 19): "Juneteenth",
    date(2023, 7, 4): "Independence Day",
    date(2023, 9, 4): "Labor Day",
    date(2023, 9, 22): "Native American Day",
    date(2023, 11, 10): "Veterans Day",
    date(2023, 11, 23): "Thanksgiving Day",
    date(2023, 11, 24): "Day after Thanksgiving",
    date(2023, 12, 25): "Christmas Day",
    date(2024, 1, 1): "New Year's Day",
    date(2024, 1, 15): "Martin Luther King, Jr. Birthday",
    date(2024, 2, 12): "Lincoln Day",
    date(2024, 2, 19): "Presidents' Day",
    date(2024, 4, 1): "Cesar Chavez Day",
    date(2024, 5, 27): "Memorial Day",
    date(2024, 6, 19): "Juneteenth",
    date(2024, 7, 4): "Independence Day",
    date(2024, 9, 2): "Labor Day",
    date(2024, 9, 27): "Native American Day",
    date(2024, 11, 11): "Veterans Day",
    date(2024, 11, 28): "Thanksgiving Day",
    date(2024, 11, 29): "Day after Thanksgiving",
    date(2024, 12, 25): "Christmas Day",
    date(2025, 1, 1): "New Year's Day",
    date(2025, 1, 20): "Martin Luther King, Jr. Birthday",
    date(2025, 2, 12): "Lincoln Day",
    date(2025, 2, 17): "Presidents' Day",
    date(2025, 3, 31): "Cesar Chavez Day",
    date(2025, 5, 26): "Memorial Day",
    date(2025, 6, 19): "Juneteenth",
    date(2025, 7, 4): "Independence Day",
    date(2025, 9, 1): "Labor Day",
    date(2025, 9, 26): "Native American Day",
    date(2025, 11, 11): "Veterans Day",
    date(2025, 11, 27): "Thanksgiving Day",
    date(2025, 11, 28): "Day after Thanksgiving",
    date(2025, 12, 25): "Christmas Day",
}

COMMON_MAIL_LOCATION_PROPERTIES = {
    "inside_CA": {"extension_days": 5, "mail_location_string": "(inside CA) "},
    "outside_CA": {
        "extension_days": 10,
        "mail_location_string": "(outside CA, within U.S.) ",
    },
    "SOS_SAHP": {
        "extension_days": 12,
        "mail_location_string": '(CA Secretary of State "Safe at Home Program") ',
    },
    "outside_US": {"extension_days": 20, "mail_location_string": "(outside of U.S.) "},
}

SERVICE_METHOD_PROPERTIES = {
    "U.S. Mail": {
        "extension_days": 5,
        "day_type": "calendar",
        "citation": "§ 1013(a)",
        "mail_location": COMMON_MAIL_LOCATION_PROPERTIES,
    },
    "Certified Mail": {
        "extension_days": 5,
        "day_type": "calendar",
        "citation": "§ 1013(a)",
        "mail_location": COMMON_MAIL_LOCATION_PROPERTIES,
    },
    "Overnight Delivery": {
        "extension_days": 2,
        "day_type": "court",
        "citation": "§ 1013(c)",
    },
    "Fax": {"extension_days": 2, "day_type": "court", "citation": "§ 1013(e)"},
    "Email": {
        "extension_days": 2,
        "day_type": "court",
        "citation": "§ 1010.6(a)(3)(B)",
    },
    "Personal": {"extension_days": 0, "day_type": "calendar", "citation": "§ 1011"},
}


def is_court_day(date: date) -> bool:
    """Check if a date is a court day (not a holiday or weekend)."""
    return date.weekday() < 5 and date not in CA_HOLIDAYS_DICT

def next_court_day(date: date) -> date:
    """Get the next court day (skip holidays and weekends)."""
    next_day = date + timedelta(days=1)
    while not is_court_day(next_day):
        next_day += timedelta(days=1)
    return next_day

def deadline_calculator_v7(
    trigger_date: date = None,
    time_period: int = None,
    service_method: str = None,
    ccp_1005_applies: bool = False,
    mail_location: str = "inside_CA",
) -> Dict[str, Union[date, str]]:
    """Calculate the deadline based on various factors."""
    try:
        # Initialize mail_location_string here (before the conditional blocks)
        service_properties = SERVICE_METHOD_PROPERTIES.get(service_method, {})
        extension_days = service_properties.get("extension_days", 0)
        day_type = service_properties.get("day_type", "calendar")
        citation = service_properties.get("citation", "§ 1011")

        # If the service method is "U.S. Mail" or "Certified Mail", further retrieve location-specific properties
        if service_method in ["U.S. Mail", "Certified Mail"]:
            mail_location_properties = service_properties.get("mail_location", {}).get(
                mail_location, {}
            )
            extension_days = mail_location_properties.get("extension_days", 0)
            mail_location_string = mail_location_properties.get(
                "mail_location_string", ""
            )
        else:
            mail_location_string = ""  # If the service method is not "U.S. Mail" or "Certified Mail", set mail_location_string to an empty string

        # Step 1: Add time_period to trigger_date
        trigger_date_plus_time_period = trigger_date + timedelta(days=time_period)

        # Add service method extension to reach initial_deadline
        if service_method in ["Overnight Delivery", "Fax", "Email"]:
            if service_method != "Email" and ccp_1005_applies:
                day_type = "calendar"
                citation = "§ 1005(b)"
                initial_deadline = trigger_date_plus_time_period + timedelta(days=extension_days)
            elif service_method == "Email" or not ccp_1005_applies:
                # Handle the special case where extension is in court days
                #if not is_court_day(trigger_date_plus_time_period):
                #    trigger_date_plus_time_period = next_court_day(trigger_date_plus_time_period)
                #    extension_days -= 1  # One day is consumed for moving to the next court day
        
                initial_deadline = trigger_date_plus_time_period
                for _ in range(extension_days):
                    initial_deadline = next_court_day(initial_deadline)
        else:
            # Standard logic for calculating the initial_deadline
            initial_deadline = trigger_date_plus_time_period + timedelta(days=extension_days)

        # Using the variables populated from the merged dictionary
        service_extension_string = (
            f"with no extension for personal service (CCP {citation})"
            if service_method == "Personal"
            else f"plus {extension_days} {day_type} days for service by {service_method} {mail_location_string}(CCP {citation})"
        )

        # Step 4: Check if the initial deadline falls on a court day
        if is_court_day(initial_deadline):
            explanation = f"Based on a service date of {trigger_date.strftime('%#m/%#d/%Y')}, adding {time_period} calendar days plus {extension_days} {day_type} days for service by {service_method} {mail_location_string}(CCP {citation}) results in a deadline of {initial_deadline.strftime('%B %#d, %Y')}."
            return {
                "datetime_obj": initial_deadline,
                "string_date": initial_deadline.strftime('%B %#d, %Y'),
                "explanation": explanation,
            }
        else:
            # Step 5: If initial deadline falls on a non-court day, roll forward to the next court day
            # Determine tense based on current date
            tense = "rolled" if initial_deadline <= date.today() else "rolls"
            tense_fall = "fell" if initial_deadline <= date.today() else "falls"
            reason = "which {} on a {}".format(
                tense_fall,
                "weekend"
                if initial_deadline.weekday() >= 5
                else CA_HOLIDAYS_DICT.get(initial_deadline, "Holiday"),
            )
            final_deadline_date = next_court_day(initial_deadline)
            explanation = (
                f"Based on a service date of {trigger_date.strftime('%#m/%#d/%Y')}, adding {time_period} calendar days "
                f"{service_extension_string} is {initial_deadline.strftime('%A, %B %#d, %Y')} {reason} and {tense} forward (§ 12a(a)) to the next court day, {final_deadline_date.strftime('%A, %B %#d, %Y')}."
            )
            return {
                "datetime_obj": final_deadline_date,
                "string_date": final_deadline_date.strftime("%A, %B %#d, %Y"),
                "explanation": explanation,
            }
    except Exception as e:
        return {
            "datetime_obj": None,
            "string_date": None,
            "explanation": f"XXXX[{type(e).__name__}]XXXX",
        }