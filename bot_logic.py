from collections import UserDict
from datetime import datetime
import re
from date_operations import get_upcoming_birthdays as get_birthdays

class Field:
    def __init__(self, value):
        if self.validate(value):
            self.value = value

    def validate(self, value):
        return True

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Value Error: Phone number must be 10 digits long")
        return True

class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            pattern = r"\d{2}\.\d{2}\.\d{4}"
            re.search(pattern, value)
            # та перетворіть рядок на об'єкт datetime
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
            
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError(f"Value Error: Phone number {old_phone} isn`t exists")

    def find_phone(self, phone) -> Phone | None:
        phones = list(filter(lambda p: p.value == phone, self.phones))
        return phones[0] if len(phones) > 0 else None 

    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))

    def find_phones(self):
        return list(map(lambda p: p.value, self.phones)) 

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)  
    
    def delete(self, name: str):
        self.data.pop(name)  
        # del self.data[name]  

    def get_upcoming_birthdays(self, days=7):
        contacts = []
        for name, record in self.data.items():
            if not record.birthday:
                continue
            contacts.append({"name": name, "birthday": record.birthday.value})

        return get_birthdays(contacts, days)


    def __str__(self):
        lines = "  Address Book\nName    Phones\n" 
        for name, numbers in self.data.items():
            # birthday = self.data[name].birthday.value if self.data[name].birthday else ''
            lines += f"{name}: {'; '.join(p_n.value for p_n in numbers.phones)}\n"

        return lines