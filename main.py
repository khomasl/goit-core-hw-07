from colorama import Fore, Style
from bot_logic import AddressBook, Record

def stylized_text(text, color=Fore.GREEN):
    return color + text + Style.RESET_ALL

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as err:
            return stylized_text(f"❌ {err}. Enter user name.", Fore.RED)
        except ValueError as err:
            return stylized_text(f"❌ {err}. Give me name and phone please or added name.", Fore.RED)  
        except AttributeError as err:
            return stylized_text(f"❌ Name '{args[0][0]}' - not found", Fore.RED)
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "✅ Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "✅ Contact added."
    if phone:
        record.add_phone(phone)
    return stylized_text(message)

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return stylized_text("✅ Contact updated.")

@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    phones = record.find_phones()
    return phones

def show_all(book: AddressBook):
    return book

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return stylized_text("✅ Birthday added.")

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record.birthday is None:
        return None
    return stylized_text(record.birthday.value)

@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


def main():
    book = AddressBook()
    
    print(stylized_text("👋 Welcome to the assistant bot! 🤖", Style.BRIGHT), end="")
    while True:
        user_input = input(stylized_text("\nEnter a command: ", Fore.CYAN))
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(stylized_text("Good bye! 👋", Style.BRIGHT))
            break

        elif command == "hello":
            print(stylized_text("How can I help you?"))
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print(stylized_text("❌ Invalid command.", Fore.RED))


if __name__ == "__main__":
    main()
