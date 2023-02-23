import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone=None):
        if re.match(r"^(096|097|098|099|050|093|073|063)\d{7}", phone):
            self.value = phone
        else:
            raise ValueError("It's not a telephone number")

class AdressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        print(dir(self.data[record.name.value]))


class Record:

    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.add_phone(phone)


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