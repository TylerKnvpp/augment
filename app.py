import os

from gmail import gmail_authenticate, handle_unread_emails
from standup import generate_standup
from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()
name = os.getenv("NAME")


def main():
    print(Fore.BLUE + f"Hello, {name}. Let's get started.")
    while True:
        print(Fore.WHITE + "\nPlease select an option: ")
        print(Fore.WHITE + "1. Check Email")
        print(Fore.WHITE + "2. Generate Standup Update")
        print(Fore.RED + "3. Exit")
        option = input(Fore.BLUE + "Enter the number of your choice: ")
        if option == "1" or option.lower() == "email":
            print(Fore.GREEN + "Authenticating", " with Gmail...")
            service = gmail_authenticate()
            print(Fore.GREEN + "Authenticated.", " Requesting unread emails...")
            if service:
                handle_unread_emails(service)
        elif option == "2" or option.lower() == "standup":
            print(Fore.GREEN + "Authenticating", " with Github...")
            generate_standup()
        elif option == "3" or option.lower() == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid option selected.")


if __name__ == "__main__":
    main()
