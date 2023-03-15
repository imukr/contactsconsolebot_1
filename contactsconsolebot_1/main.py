from func import extracting_commands, contacts

def main():
    try:
        while True:
            user_date = input("Enter set of command: ")
            result = extracting_commands(user_date)
            print(result)
            if result == 'Good bye':
                break
    finally:
        contacts.save_contacts_to_file()

if __name__ == '__main__':
    main()
