import os
import speech_recognition as sr
import speech_recognition as sr

from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()

MIC_INDEX = os.getenv("MIC_INDEX")


def get_speech_input():
    tries = 0
    r = sr.Recognizer()

    if MIC_INDEX:
        print(
            Fore.WHITE + "Using microphone: ",
            sr.Microphone.list_microphone_names()[MIC_INDEX],
        )
        mic = sr.Microphone(device_index=int(MIC_INDEX))
    else:
        print(
            Fore.WHITE + "Using microphone: ", sr.Microphone.list_microphone_names()[0]
        )
        mic = sr.Microphone(device_index=0)

    with mic as source:
        print(Fore.BLUE + "Talk")
        r.adjust_for_ambient_noise(source)  # Adjusts the level to account for noise
        try:
            audio_text = r.listen(source, timeout=7)  # Listen to the source
        except sr.WaitTimeoutError:
            print(Fore.RED + "Timeout error: No speech detected. Trying again...")
            tries += 1
            if tries < 3:
                get_speech_input()
            else:
                return print(Fore.RED + "Mic timed out.")

    try:
        transcribed_text = r.recognize_google(audio_text)
        print(Fore.GREEN + "You Said: ")
        print(
            Fore.WHITE + transcribed_text
        )  # Recognize speech using Google Speech Recognition
        return transcribed_text
    except sr.UnknownValueError:
        print(Fore.RED + "Google Speech Recognition could not understand the audio.")
        get_speech_input()
    except sr.RequestError as e:
        print(
            Fore.RED
            + f"Could not request results from Google Speech Recognition service; {e}"
        )
        get_speech_input()
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
