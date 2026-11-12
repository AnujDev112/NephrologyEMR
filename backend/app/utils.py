from datetime import date


def calculate_age(dob: date, on: date | None = None) -> int:
    on = on or date.today()
    years = on.year - dob.year
    if (on.month, on.day) < (dob.month, dob.day):
        years -= 1
    return years
