from datetime import datetime, date, timedelta

def string_to_date(string):
    return datetime.strptime(string, "%d.%m.%Y").date()

def date_to_string(date):
    return date.strftime("%d.%m.%Y")

def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday

def get_upcoming_birthdays(contacts, days=7):
    upcoming_birthdays = []
    today = date.today()
    
    for contact in contacts:
        birthday_this_year = string_to_date(contact["birthday"]).replace(year=today.year)

        """
        Додайте на цьому місці перевірку, чи не буде 
        припадати день народження вже наступного року.
        """
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            

        if 0 <= (birthday_this_year - today).days <= days:
            """ 
            Додайте перенесення дати привітання на наступний робочий день,
            якщо день народження припадає на вихідний. 
            """
            birthday_this_year = adjust_for_weekend(birthday_this_year)

            congratulation_date_str = date_to_string(birthday_this_year)
            upcoming_birthdays.append({"name": contact["name"], "birthday": congratulation_date_str})
    return upcoming_birthdays
