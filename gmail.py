import os.path
import base64
import pickle
import html

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from bs4 import BeautifulSoup, Tag
from colorama import Fore, Style

# Load the environment variables from the .env file
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

prompt = PromptTemplate(
    input_variables=["email"],
    template="Try your best to summarize this email {email}?",
)

llm = OpenAI(temperature=0.9, openai_api_key=API_KEY)

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def gmail_authenticate():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )  # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        return None


def get_unread_messages(service):
    results = (
        service.users()
        .messages()
        .list(userId="me", q="is:unread in:inbox -category:promotions")
        .execute()
    )
    return results.get("messages", [])


def get_message(service, msg_id):
    try:
        message = service.users().messages().get(userId="me", id=msg_id).execute()
        return message
    except Exception as error:
        print(Fore.RED + f"An error occurred: {error}")
        return None


def parse_email_headers(email_data):
    sender = ""
    subject = ""
    for values in email_data:
        name = values["name"]
        if name == "Subject":
            subject = values["value"]
        if name == "From":
            sender = values["value"]
    return sender, subject


def parse_email_body(part):
    data = part["body"]["data"]
    data = data.replace("-", "+").replace("_", "/")
    decoded_data = base64.b64decode(data)
    email = decoded_data.decode("utf-8")
    return email


def clean_email_content(email):
    soup = BeautifulSoup(email, "html.parser")
    for a in soup.findAll("a"):
        a.decompose()
    email = soup.get_text(separator=" ")
    email = html.unescape(email)
    email = " ".join(email.split())
    return email


def archive_email(service, message_id):
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD", "INBOX"]},
    ).execute()


def parse_message(msg):
    email_data = msg["payload"]["headers"]
    for values in email_data:
        name = values["name"]
        if name == "Subject":
            subject = values["value"]
        if name == "From":
            sender = values["value"]
    return subject, sender


def truncate_email(email, max_length=4097, safety_margin=1000):
    tokens = email.split()
    if len(tokens) > max_length - safety_margin:
        tokens = tokens[: (max_length - safety_margin)]
    return " ".join(tokens)


def handle_unread_emails(service):
    try:
        messages = get_unread_messages(service)

        if not messages:
            print(Fore.WHITE + "No new messages.")
        else:
            for message in messages:
                msg = get_message(service, message["id"])
                sender, subject = parse_message(msg)

                # Parsing the email body
                if "parts" in msg["payload"]:
                    part = msg["payload"]["parts"][0]
                    email = parse_email_body(part)
                    email = clean_email_content(email)
                    email = truncate_email(email)
                else:
                    email = "No body found in the email."

                print(Fore.WHITE + "From: ", sender)
                print(Fore.WHITE + "Subject: ", subject)
                print(
                    Fore.BLUE
                    + "Do you want to read, archive, move to the next email or do something else?"
                )
                action = input("(read/archive/next/do something else): ").lower()
                if action == "read":
                    print(Fore.GREEN + "Summarizing with GPT...")
                    chain = LLMChain(llm=llm, prompt=prompt)
                    try:
                        chain = LLMChain(llm=llm, prompt=prompt)
                        summary = chain.run(email)
                        print(Fore.WHITE + "Summary:", summary)
                    except Exception as e:
                        print(
                            Fore.RED
                            + f"An error occurred while summarizing the email: {e}"
                        )
                        print(Fore.WHITE + "Skipping to the next email...")
                        continue

                    # This will mark the message as read
                    service.users().messages().modify(
                        userId="me",
                        id=message["id"],
                        body={"removeLabelIds": ["UNREAD"]},
                    ).execute()

                    print(
                        Fore.BLUE
                        + "Do you want to archive this email or move to the next one?"
                    )
                    action_after_read = input("(archive/next): ").lower()
                    if action_after_read == "archive":
                        # This will remove the message from the inbox
                        service.users().messages().modify(
                            userId="me",
                            id=message["id"],
                            body={"removeLabelIds": ["INBOX"]},
                        ).execute()
                        print(Fore.GREEN + "Email archived.")
                    elif action_after_read == "next":
                        print(Fore.WHITE + "Moving to the next email...")
                    else:
                        print(Fore.RED + "Invalid input. Skipping this email.")
                elif action == "archive":
                    # This will mark the message as read and remove it from the inbox
                    service.users().messages().modify(
                        userId="me",
                        id=message["id"],
                        body={"removeLabelIds": ["UNREAD", "INBOX"]},
                    ).execute()
                    print(Fore.RED + "Email archived.")
                elif action == "next":
                    print(Fore.WHITE + "Moving to the next email...")
                elif action == "do something else":
                    return
                else:
                    print(Fore.RED + "Invalid input. Skipping this email.")
    except Exception as error:
        print(Fore.RED + f"An error occurred: {error}")
