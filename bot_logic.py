from datetime import datetime
from colorama import Fore, Style
from collections import UserDict
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
            datetime.strptime(value, "%d.%m.%Y").date()
            self.value = value
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
        return Fore.YELLOW + f"Contact name: {self.name.value}, birthday: {self.birthday}, phones: {'; '.join(p.value for p in self.phones)}" + Style.RESET_ALL

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
        # lines = "     Address Book\nName   Birthday    Phones\n" 
        # for name, record in self.data.items():
        #     birthday = record.birthday.value if record.birthday else ' '*10
        #     lines += f"{name}: {birthday}  {'; '.join(pone.value for pone in record.phones)}\n"
        
        # return lines
        
        print(Style.BRIGHT + "       Address Book" + Style.RESET_ALL)
        for name, record in self.data.items():
            print(record)
        
        return ''   