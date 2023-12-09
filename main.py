# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3
import openai
from elevenlabs import generate, play
import keyboard

openai.api_key = "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"

# Initialize the recognizer
r = sr.Recognizer()

current_Chat = []


# Function to convert text to speech
def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()

    # Sets Volume and speed rate of speech
    engine.setProperty("volume", 0.8)
    engine.setProperty('rate', 150)

    # Set the voice for female
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    engine.say(command)
    engine.runAndWait()


# Better Voices from Eleven Labs
def better_voice(text):
    audio = generate(
        text=text,
        voice="Bella",
        model="eleven_multilingual_v2"
    )
    play(audio)


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


# Loop infinitely for user to speak
while 1:

    if keyboard.read_key() == "0":
        listen_user()
