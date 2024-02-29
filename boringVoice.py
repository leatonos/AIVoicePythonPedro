# Function to convert text to speech (HAS VERY BAD VOICE)
import pyttsx3


def speak_text(text: str):
    """
    This is a VERY boring speaking
    :param text: The text that will be read by python TTS
    :return:
    """

    # Initialize the engine
    engine = pyttsx3.init()

    # Sets Volume and speed rate of speech
    engine.setProperty("volume", 0.8)
    engine.setProperty('rate', 150)

    # Set the voice for female
    bad_voices = engine.getProperty('voices')
    engine.setProperty('voice', bad_voices[1].id)

    engine.say(text)
    engine.runAndWait()
