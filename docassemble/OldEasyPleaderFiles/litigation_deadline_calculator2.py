__all__ = ['deadline_calculator_v4']

import datetime

# Define California state holidays between 2023 and 2025
CA_HOLIDAYS_DICT = {
    datetime.date(2023, 1, 2): "New Year's Day",
    datetime.date(2023, 1, 16): "Martin Luther King, Jr. Birthday",
    datetime.date(2023, 2, 13): "Lincoln Day",
    datetime.date(2023, 2, 20): "Presidents' Day",
    datetime.date(2023, 3, 31): "Cesar Chavez Day",
    datetime.date(2023, 5, 29): "Memorial Day",
    datetime.date(2023, 6, 19): "Juneteenth",
    datetime.date(2023, 7, 4): "Independence Day",
    datetime.date(2023, 9, 4): "Labor Day",
    datetime.date(2023, 9, 22): "Native American Day",
    datetime.date(2023, 11, 10): "Veterans Day",
    datetime.date(2023, 11, 23): "Thanksgiving Day",
    datetime.date(2023, 11, 24): "Day after Thanksgiving",
    datetime.date(2023, 12, 25): "Christmas Day",
    datetime.date(2024, 1, 1): "New Year's Day",
    datetime.date(2024, 1, 15): "Martin Luther King, Jr. Birthday",
    datetime.date(2024, 2, 12): "Lincoln Day",
    datetime.date(2024, 2, 19): "Presidents' Day",
    datetime.date(2024, 4, 1): "Cesar Chavez Day",
    datetime.date(2024, 5, 27): "Memorial Day",
    datetime.date(2024, 6, 19): "Juneteenth",
    datetime.date(2024, 7, 4): "Independence Day",
    datetime.date(2024, 9, 2): "Labor Day",
    datetime.date(2024, 9, 27): "Native American Day",
    datetime.date(2024, 11, 11): "Veterans Day",
    datetime.date(2024, 11, 28): "Thanksgiving Day",
    datetime.date(2024, 11, 29): "Day after Thanksgiving",
    datetime.date(2024, 12, 25): "Christmas Day",
    datetime.date(2025, 1, 1): "New Year's Day",
    datetime.date(2025, 1, 20): "Martin Luther King, Jr. Birthday",
    datetime.date(2025, 2, 12): "Lincoln Day",
    datetime.date(2025, 2, 17): "Presidents' Day",
    datetime.date(2025, 3, 31): "Cesar Chavez Day",
    datetime.date(2025, 5, 26): "Memorial Day",
    datetime.date(2025, 6, 19): "Juneteenth",
    datetime.date(2025, 7, 4): "Independence Day",
    datetime.date(2025, 9, 1): "Labor Day",
    datetime.date(2025, 9, 26): "Native American Day",
    datetime.date(2025, 11, 11): "Veterans Day",
    datetime.date(2025, 11, 27): "Thanksgiving Day",
    datetime.date(2025, 11, 28): "Day after Thanksgiving",
    datetime.date(2025, 12, 25): "Christmas Day"
}

def is_business_day(date):
    """Check if a date is a business day.
    
    Args:
        date (datetime.date): The date to check.
        
    Returns:
        bool: True if the date is a business day, False otherwise.
    """
    return date.weekday() < 5 and date not in CA_HOLIDAYS_DICT

def next_business_day(date):
    """Get the next business day after a given date.
    
    Args:
        date (datetime.date): The starting date.
        
    Returns:
        datetime.date: The next business day.
    """
    next_day = date + datetime.timedelta(days=1)
    while not is_business_day(next_day):
        next_day += datetime.timedelta(days=1)
    return next_day

def deadline_calculator_v4(trigger_date, number_of_days, service_method):
    """Calculate the deadline based on a trigger date, number of days, and service method.
    
    Args:
        trigger_date (datetime.date): The date the event was triggered.
        number_of_days (int): The number of days from the trigger date.
        service_method (str): The method of service. Options include "mail", "overnight delivery", "email", "fax", and "personal".
        
    Returns:
        str: A string indicating the final deadline date, and reasons for any adjustments if applicable.
    """
    # Determine raw deadline
    raw_deadline = trigger_date + datetime.timedelta(days=number_of_days)
    
    # Add days based on service method
    if service_method == "U.S. Mail" or "Certified Mail":
        initial_deadline_date = raw_deadline + datetime.timedelta(days=5)
    elif service_method == "Overnight Delivery":
        initial_deadline_date = raw_deadline + datetime.timedelta(days=2)
    elif service_method in ["Email", "Fax"]:
        # Add business days
        initial_deadline_date = raw_deadline
        added_days = 0
        while added_days < 2:
            initial_deadline_date += datetime.timedelta(days=1)
            if is_business_day(initial_deadline_date):
                added_days += 1
    elif service_method == "Personal":
        initial_deadline_date = raw_deadline
    else:
        raise ValueError(f"Invalid service method: {service_method}")
    
    # Format date without leading zero
    formatted_initial_date = initial_deadline_date.strftime('%A, %B %-d, %Y')
    
    # Check if the initial deadline date is a business day
    if is_business_day(initial_deadline_date):
        return formatted_initial_date
    else:
        reason = f"The initial deadline date was {formatted_initial_date}. "
        if initial_deadline_date.weekday() >= 5:
            reason += "It fell on a weekend "
        else:
            holiday_name = CA_HOLIDAYS_DICT.get(initial_deadline_date, "Holiday")
            reason += f"It fell on {holiday_name} "
        final_deadline_date = next_business_day(initial_deadline_date)
        reason += f"and rolled forward to the next business day, {final_deadline_date.strftime('%A, %B %-d, %Y')}."
        return reason
