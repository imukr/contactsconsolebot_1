from collections import UserDict, UserList

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass


class Phone(Field):
    pass

class AdressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        # print(dir(self.data[record.name.value]))


class Record:

    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []



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