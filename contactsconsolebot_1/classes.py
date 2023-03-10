from datetime import datetime
from collections import UserDict
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
        date_format = '%d.%m.%Y'

        try:
            date_birthday = datetime.strptime(value, date_format)
            self._value = date_birthday.date()

        except TypeError:

            raise TypeError(
                "Incorrect data format for birthday, should be DD.MM.YYYY")


class AdressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_record(self, name):
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def get_all_record(self):
        return '\n'.join([f'Contact {name} have a phone/es {" ".join([phone.value for phone in data.phones])} and have a birthday {data.birthday.value}' for name, data in
                          self.data.items()])

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
        for elem in self.phones:
            if elem.value == phone:
                self.phones.remove(elem)


    def change_phone(self, old_phone, new_phone):
        for elem in self.phones:
            if elem.value == old_phone:
                elem.value = new_phone

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
        phones_info = ''
        birthday_info = ''

        for phone in self.phones:
            phones_info += f'{phone.value}, '

        if self.birthday:
            birthday_info = f' Birthday : {self.birthday.value}'

        return f'{self.name.value} : {phones_info[:-2]}{birthday_info}'