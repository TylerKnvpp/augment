import os

from gmail import gmail_authenticate, handle_unread_emails
from standup import generate_standup
from colorama import Fore, Style
from dotenv import load_dotenv
from speech import get_speech_input

load_dotenv()
name = os.getenv("NAME")


def text_prompts():
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
                handle_unread_emails(service, False)
        elif option == "2" or option.lower() == "standup":
            print(Fore.GREEN + "Authenticating", " with Github...")
            generate_standup(False)
        elif option == "3" or option.lower() == "exit":
            print("Exiting...")
            break
        else:
            print("Invalid option selected.")


def voice_prompts():
    while True:
        print(Fore.WHITE + "\nPlease select an option: ")
        print(Fore.WHITE + "1. Check Email")
        print(Fore.WHITE + "2. Generate Standup Update")
        print(Fore.RED + "3. Exit")
        option = get_speech_input()
        if option == "1" or "email" in option.lower():
            print(Fore.GREEN + "Authenticating", " with Gmail...")
            service = gmail_authenticate()
            print(Fore.GREEN + "Authenticated.", " Requesting unread emails...")
            if service:
                handle_unread_emails(service, True)
        elif (
            option == "2" or "standup" in option.lower() or "stand up" in option.lower()
        ):
            print(Fore.GREEN + "Authenticating", " with Github...")
            generate_standup(True)
        elif option == "3" or "exit" in option.lower():
            print("Exiting...")
            break
        else:
            print("Invalid option selected. Try again.")


def main():
    print(Fore.BLUE + f"Hello, {name}. Let's get started.")
    should_use_voice = input(
        Fore.BLUE + "Would you like to use voice input? (y/n): "
    ).lower()
    if should_use_voice == "y":
        voice_prompts()
    else:
        text_prompts()


if __name__ == "__main__":
    main()
