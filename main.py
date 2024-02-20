# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
from elevenlabs import generate, play, voices
from elevenlabs.client import ElevenLabs
import keyboard
import pprint

# API key config
import os
load_dotenv()
openai_api_key = os.environ.get('OPENAI_API_KEY')
elevenlabs_api_key = os.environ.get('ELEVEN_API_KEY')
openai.api_key = openai_api_key
client = ElevenLabs(api_key=elevenlabs_api_key)

# Initialize the recognizer
r = sr.Recognizer()

current_Chat = []
default_voice = "Rachel"


# Function to convert text to speech
def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()

    # Sets Volume and speed rate of speech
    engine.setProperty("volume", 0.8)
    engine.setProperty('rate', 150)

    # Set the voice for female
    bad_voices = engine.getProperty('voices')
    engine.setProperty('voice', bad_voices[1].id)

    engine.say(command)
    engine.runAndWait()


# Better Voices from Eleven Labs
def better_voice(text):
    audio = generate(
        text=text,
        voice=default_voice,
        model="eleven_multilingual_v2",
        # api_key=elevenlabs_api_key
    )

    play(audio)


def list_voices():
    pp = pprint.PrettyPrinter(indent=4)
    all_voices = voices()
    # pp.pprint(all_voices)
    for voice in all_voices:
        this_voice = \
            (f"{voice.name}: "
             f"Gender:{voice.labels['gender']}, "
             f"Accent:{voice.labels['accent']}, "
             f"Age:{voice.labels['age']}, ")
        print(this_voice)


def change_voice():
    all_voices = voices()
    print("")

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


def confirm_voice(voice_name: str):
    global default_voice
    default_voice = voice_name
    print(f"Hello, my name is {voice_name}, and this is my voice.")
    better_voice(f"Hello, my name is {voice_name}, and this is my voice.")
    user_input = input(f"Confirm your choice pressing entering Y or anything else to choose another voice.")
    if user_input == 'Y' or user_input == 'y':
        print('Voice changed!')
    else:
        change_voice()


# ChatGPT function
def chat_ai():
    print("Chat Gpt is processing a response...")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=150,
        messages=current_Chat
    )

    ai_result = completion.choices[0].message.content

    print(completion.choices[0].message.content)
    better_voice(ai_result)
    # Adds the AI to the current chat so you can keep context to the conversation
    current_Chat.append({"role": "assistant", "content": ai_result})


# Function that listen to the User
def listen_user():
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
            current_Chat.append({"role": "user", "content": MyText})
            chat_ai()

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    except sr.UnknownValueError:
        print("unknown error occurred")


def print_menu():
    print("AI voice program Menu")
    print("Options:")
    print(">> Start listening: 0")
    print(">> List all voices: 1")
    print(">> Choose new Voice: 2")


# Loop infinitely for user to speak
print_menu()
while True:

    option = keyboard.read_key()

    if option == "0":
        listen_user()
    elif option == "1":
        list_voices()
    elif option == "2":
        list_voices()
        change_voice()
