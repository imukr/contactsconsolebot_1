from func import extracting_commands

def main():
    while True:
        user_date = input("Enter set of command: ")
        result = extracting_commands(user_date)
        print(result)

if __name__ == '__main__':
    main()
