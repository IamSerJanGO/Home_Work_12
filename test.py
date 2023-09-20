from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class AddressBook(UserDict):

    def add_record(self, Record):
        self.data[Record.name.value] = Record

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        address_book =  cls()
        address_book.data = data
        return address_book

    def search(self, query):
        result = []
        for name, record in self.data.items():
            if query in name:
                result.append(record)
            for phone in record.value:
                if query in phone.value:
                    result.append(record)
        return result





class Record:
    def __init__(self, Name, Birthday=None):
        self.name = Name
        self.phones = []
        self.birthday = Birthday

    def add_phone(self, Phone):
        self.phones.append(Phone)

    def remove_phone(self, Phone_remuove):
        for Phone in self.phones:
            if Phone.value == Phone_remuove:
                self.phones.remove(Phone)

    def change_phone(self, old_phone, new_phone):
        for Phone in self.phones:
            if Phone == old_phone:
                self.phones.remove(Phone)
                self.phones.append(new_phone)

    def add_birthday(self, Birthday):
        self.birthday = Birthday

    def days_to_birthday(self):
        birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()
        today = datetime.now().date()
        birthday = birthday.replace(year=today.year)
        if birthday < today:
            birthday = birthday.replace(year=today.year + 1)
        return (birthday - today).days


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()


class Name(Field):
    pass


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        try:
            birthday = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            birthday = None
        if birthday is not None and birthday < today:
            self._value = value
        else:
            raise BirthdayInvalidFormatError('Invalid birthday format')


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if value.startwith('+') and len(value[1:]) == 12 and value[1:].isdigit() or value.isdigit() and len(value) in (10, 12):
            self._value = value
        else:
            raise PhoneInvalidFormatError('Invalid phone format')


class PhoneInvalidFormatError(Exception):
    pass


class BirthdayInvalidFormatError(Exception):
    pass


address_book = AddressBook()








phone_book = {}


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Error: contact not found.'
        except ValueError:
            return "Error: Invalid input. Please enter name and phone number."
        except IndexError:
            return "Error: Invalid input. Please enter name and phone number."

    return inner


@input_error
def chenge(name, number):
    if name not in phone_book:
        raise KeyError
    else:
        phone_book[name] = number
        return f'New number contact {name} is {number}'


@input_error
def add_contact(name, number):
    if name in phone_book:
        raise ValueError
    else:
        phone_book[name] = number
        return f'New contact {name} with number {number} - created!'


@input_error
def phone_check(name):
    if name not in phone_book:
        raise KeyError
    else:
        return f'Contact {name} number : {phone_book[name]}'


@input_error
def show_phone_book():
    if not phone_book:
        raise ValueError
    else:
        contact = 'Contact\n'
        for name, number in phone_book.items():
            contact += f'{name} : {number}'
    return contact


def main():
    commands = {
        "hello": lambda: print("How can I help you?"),
        "add": lambda: print(add_contact(devided_user_input[1], devided_user_input[2])) if len(
            devided_user_input) == 3 else print('Error: enter '
                                                'name and '
                                                'number'),
        "change": lambda: print(chenge(devided_user_input[1], devided_user_input[2])) if len(devided_user_input) == 3
        else print('Error: enter name and number'),
        "phone": lambda: print(phone_check(devided_user_input[1])) if len(devided_user_input) == 2 else print(
            'Contact not found'),
        "show all": lambda: print(show_phone_book()) if phone_book else print('Your phone book is empty :('),
        "good bye": lambda: print("Good bye!"),
        "close": lambda: print("Good bye!"),
        "exit": lambda: print("Good bye!"),
        "save": lambda: address_book.save_to_file("address_book.pickle"),
        "load": lambda: load_address_book(),
        "search": lambda: search_contacts(),
    }
    while True:
        user_input = input('Enter your command: ')
        devided_user_input = user_input.split(maxsplit=2)
        user_command = devided_user_input[0].strip().lower()

        if user_command in commands:
            commands[user_command]()
            if user_command in ['close', 'exit']:
                break
        elif user_input.lower() in commands:
            commands[user_input.lower()]()
            if user_input.lower() == 'good bye':
                break
        else:
            print('Invalid input command. Available commands: hello/add/change/phone/show all/good bye/close/exit')

    def load_address_book():
        global address_book
        try:
            address_book = AddressBook.load_from_file("address_book.pickle")
            print("Address book loaded successfully.")
        except FileNotFoundError:
            print("Address book not found.")

    def search_contacts():
        query = input("Enter a name or phone number to search for: ")
        results = address_book.search(query)
        if results:
            print("Search results:")
            for record in results:
                print(f"Name: {record.name.value}")
                for phone in record.phones:
                    print(f"Phone: {phone.value}")
        else:
            print("No matching contacts found.")

if __name__ == '__main__':
    main()
