from collections import UserDict
from contextlib import suppress
from datetime import datetime
import pickle
import re


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


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if re.match(r"^(096|097|098|099|050|093|073|063)\d{7}", value):
            self._value = value
        else:
            raise ValueError("It's not a telephone number")


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        birth_date = datetime.strptime(value, '%Y-%m-%d').date()
        if birth_date > today:
            raise ValueError("Birthday must be less than current year and date.")
        self._value = value


class AdressBook(UserDict):

    def __init__(self):
        super().__init__()

        self.load_contacts_from_file()

    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        record_result = []
        for record in self.data.values():
            if value in record.name.value:
                record_result.append(record)
                continue

            for phone in record.phones:
                if value in phone.value:
                    record_result.append(record)

        if not record_result:
            raise ValueError("Contacts with this value does not exist.")
        return record_result

    def iterator(self, count=5):
        page = []
        i = 0

        for record in self.data.values():
            page.append(record)
            i += 1

            if i == count:
                yield page
                page = []
                i = 0

        if page:
            yield page

    def save_contacts_to_file(self):
        with open('address_book.txt', 'wb') as file:
            pickle.dump(self.data, file)

    def load_contacts_from_file(self):
        with suppress(FileNotFoundError):
            with open('address_book.txt', 'rb') as file:
                self.data = pickle.load(file)


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if phone:
            self.add_phone(phone)
        if birthday:
            self.add_birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for phone in self.phones:
            if phone.value == phone:
                self.phones.remove(phone)

    def change_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def day_to_birthday(self):
        if not self.birthday:
            raise ValueError("This contact doesn't have attribute birthday")
        today = datetime.now().date()
        birthday = self.birthday.value
        next_birthday_year = today.year
        if today.month >= birthday.month and today.day > birthday.day:
            next_birthday_year += 1
        next_birthday = datetime(year=next_birthday_year, month=birthday.month, day=birthday.day)
        return (today - next_birthday.date()).days

    def get_info(self):
        birthday_info = ''

        phones_info = [phone.value for phone in self.phones]

        if self.birthday:
            birthday_info = f' Birthday : {self.birthday.value}'

        return f'{self.name.value} : {phones_info}{birthday_info}'
