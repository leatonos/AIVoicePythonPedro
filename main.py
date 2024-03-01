# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import openai
import ElevenLabsVoice
from dotenv import load_dotenv
from elevenlabs import voices
from elevenlabs.client import ElevenLabs
import keyboard

# API key config
# IN ORDER TO MAKE THIS APP WORK YOU NEED TO SET UP THIS
# You will need Eleven labs api key and a ChatGPT api key
import os

import boringVoice
from AIChat import get_ai_response, start_robot_conversation

load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
elevenlabs_api_key = os.environ.get('ELEVEN_API_KEY')
client = ElevenLabs(api_key=elevenlabs_api_key)
openai.api_key = openai_api_key

# Initialize the voice recognizer
r = sr.Recognizer()

initial_context = ""

solo_current_chat = [
    {"role": "system", "content": initial_context}
]
default_voice = "Rachel"


def confirm_voice(chosen_voice):
    test_text = f"Hello my name {chosen_voice}, and this is my voice"
    ElevenLabsVoice.better_voice(test_text, chosen_voice, elevenlabs_api_key)

    user_input = input("Confirm your choice by inputting Y or anything else to choose a new voice")
    if str(user_input) == "Y":
        global default_voice
        default_voice = str(user_input)
        print("Voice changed!")


def change_voice():
    all_voices = voices()

    user_input = input("Type the name of the voice you want: ")
    print(f"You entered {user_input}")

    chosen_voice = str(user_input)

    voice_found = False
    for voice in all_voices:
        if voice.name == chosen_voice:
            print("Voice Found!")
            voice_found = True

    if voice_found:
        confirm_voice(chosen_voice)
    else:
        print("Voice not found try again...")


# Function that listen to the User
def listen_user():
    """
    Uses your Microphone to listen your voice, after some seconds of silence it translate
    your message to text, adds your text to a conversation log, then sends it to ChatGPT
    """

    print("Listening to user")
    # Exception handling to handle
    # exceptions at the runtime
    try:

        # use the microphone as source for input.
        with sr.Microphone() as source2:

            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)

            # listens for the user's input
            audio2 = r.listen(source2)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()

            print("Chat GPT heard: ", MyText)

            # Add user's message to the current chat
            solo_current_chat.append({"role": "user", "content": MyText})

            # Gets the AI Response and add to the the current Chat
            ai_response = get_ai_response(solo_current_chat)
            solo_current_chat.append({"role": "assistant", "content": ai_response})

            # Plays the response using a voice that you choose in Eleven Labs
            ElevenLabsVoice.better_voice(ai_response, default_voice, elevenlabs_api_key)

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


def setup_bot_conversation():
    """
    Starts some prompts so the user can write about the robots that will start a conversation
    """

    robots_context = {'robot_a': "", 'robot_b': ""}

    first_robot_input = input("Describe the first Robot")
    robots_context["robot_a"] = str(first_robot_input)

    second_robot_input = input("Describe the second Robot")
    robots_context["robot_b"] = str(second_robot_input)

    rounds_input = input("How many rounds this conversation will have?")
    rounds_number = int(rounds_input)

    print("This will be the context of the conversation: \n")
    print(f"Robot A: \n {robots_context['robot_a']}")
    print(f"Robot B: \n {robots_context['robot_b']}")

    start_robot_conversation(robots_context['robot_a'], robots_context['robot_b'], rounds_number, elevenlabs_api_key)


def print_menu():
    """
    Prints in the console all the options you have in this program
    :return:
    """

    print("AI voice program Menu")
    print("Options:")
    print(">> Start listening: 0")
    print(">> List all voices: 1")
    print(">> Choose new Voice: 2")
    print(">> Get Subscription Status: 3")
    print(">> Start Robot Dialog: 4")


# Loop infinitely for user to speak
print_menu()

while True:

    option = keyboard.read_key()

    if option == "0":
        listen_user()
    elif option == "1":
        ElevenLabsVoice.list_voices()
    elif option == "2":
        ElevenLabsVoice.list_voices()
        change_voice()
    elif option == "3":
        ElevenLabsVoice.print_sub_status(elevenlabs_api_key)
    elif option == "4":
        setup_bot_conversation()
