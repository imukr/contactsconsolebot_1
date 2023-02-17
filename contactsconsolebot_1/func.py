from classes import AdressBook, Record


contacts = AdressBook()


def exepting(func): #catching errors
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Please print: name and number'
        except TypeError:
            return 'Wrong command.'
    return inner


@exepting
def hello():
    return 'Can I help You'


@exepting
def add(name, phone=None): #add data to phone book
    if name in contacts:
        contacts[name].add_phone(phone)
        return 'You add phone {phone} to {name}'
    record = Record(name, phone)
    contacts.add_record(record)
    return f'You added {name} with contact {phone}'


@exepting #change phone numbers of contact
def change(name, old_phone, new_phone):
    contacts[name].change_phone(old_phone, new_phone)
    return f'You changed phone {old_phone} to {new_phone}'


@exepting #output phone numbers of contact
def what_phone(name):
    for key, data in contacts.items():
        if key == name:
            return f'Contact {name} have phone/es {" ".join([phone.value for phone in data.phones])}'
    return "No such name"


@exepting #Show contacts
def show_all(*args):
    return '\n'.join([f'Name {name}: phone/es {" ".join([phone.value for phone in data.phones])}' for name, data in contacts.items()])

@exepting
def exiting():
    return 'Good bye'

@exepting
def deliting(name, phone):
    contacts[name].remove_phone(phone)
    return f'You delited phone {phone}'

'''
commands for using same functions
'''
commands = {
    "hello": hello,
    "add": add,
    "change": change,
    "show all": show_all,
    "what phone": what_phone,
    "good bye": exiting,
    "delite": deliting,
    "exit": exiting
}


# @exepting
def extracting_commands(entered_data):
    set_commands = entered_data.lower().strip()
    for command in commands:
        if set_commands.startswith(command):
            return commands[command](*((set_commands[len(command):]).strip().split()))
    return 'Wrong command'