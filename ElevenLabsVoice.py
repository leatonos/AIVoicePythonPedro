import pprint

from elevenlabs import generate, play, voices
from elevenlabs.client import ElevenLabs


def better_voice(text: str, voice: str, api_key: str):
    """

    Uses Eleven Labs API to generate and play voices
    :param api_key: Your API key for Eleven Labs
    :param text: The text that will be read by Eleven Labs
    :param voice: The name of the voice you choose to read the text (check the API to see the voices available

    """

    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2",
        # api_key=api_key
    )

    play(audio)
    print(f"Your Account have {get_characters_left(api_key)} left.")


def get_characters_left(api_key):
    client = ElevenLabs(api_key=api_key)

    """
    :return: How many characters you have left in your monthly Eleven Labs Subscription
    """

    character_count = client.user.get_subscription().character_count
    character_limit = client.user.get_subscription().character_limit
    character_left = character_limit - character_count
    return character_left


def list_voices():
    """
    Prints in the console all the voices available in Eleven Labs
    :return:
    """

    all_voices = voices()

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(all_voices)
    for voice in all_voices:
        this_voice = \
            (f"{voice.name}: "
             f"Gender:{voice.labels['gender']}, "
             f"Accent:{voice.labels['accent']}, "
             f"Age:{voice.labels['age']} ")
        #    f"Description:{voice.labels['description']}, ")
        print(this_voice)


def print_sub_status(api_key):
    """
    Prints some information about your subscription to
    :return:
    """

    client = ElevenLabs(api_key=api_key)

    subscription_tier = client.user.get_subscription().tier
    character_count = client.user.get_subscription().character_count
    character_limit = client.user.get_subscription().character_limit

    character_left = character_limit - character_count

    print(
        f"\n"
        f"User Subscription: {subscription_tier} \n"
        f"Characters count: {character_count}, "
        f"Characters limit: {character_limit}, "
        f"Characters left: {character_left}"
    )
