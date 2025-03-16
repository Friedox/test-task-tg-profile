from datetime import date


def calculate_countdown(birthday: date) -> str:
    today = date.today()
    next_birthday = birthday.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)
    delta = next_birthday - today
    return f"{delta.days} дней"
