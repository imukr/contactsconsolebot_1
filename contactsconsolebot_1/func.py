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
def add(name, phone=None, birthday=None): #add data to phone book
    if name in contacts:
        contacts[name].add_phone(phone)
        return f'You add phone {phone} to {name}'
    record = Record(name, phone, birthday)
    contacts.add_record(record)
    return f'You added {name} with contact {phone} and birthday {birthday}'


@exepting #change phone numbers of contact
def change_phone(name, old_phone, new_phone):
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
    contact_list = ''
    page_number = 1
    for page in contacts.iterator():
        contact_list += f'Page #{page_number}\n'
        for record in page:
            contact_list += f'{record.get_info()}\n'
        page_number += 1
    return contact_list


@exepting
def deliting_phone(name, phone):
    contacts[name].remove_phone(phone)
    return f'You delited phone {phone}'


def day_to_birthday (name):
    record = contacts[name]
    return f"Days to next birthday of this {name} will be in {record.day_to_birthday()}."


@exepting
def exiting():
    return 'Good bye'



'''
commands for using same functions
'''
commands = {
    "hello": hello,
    "add": add,
    "change_phone": change_phone,
    "what phone": what_phone,
    "show all": show_all,
    "delite_phone": deliting_phone,
    "day": day_to_birthday,
    "good bye": exiting,
    "exit": exiting
}



def extracting_commands(entered_data):
    set_commands = entered_data.lower().strip()
    for command in commands:
        if set_commands.startswith(command):
            return commands[command](*((set_commands[len(command):]).strip().split()))
    return 'Wrong command'