import os
import openai

import boringVoice

openai_api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = openai_api_key


def get_ai_response(conversation):
    """
    Sends the current conversation to ChatGPT and awaits a response
    after that gets the response and uses Eleven labs to read the message for you
    :param conversation:
    :return:
    """
    print("Chat Gpt is processing a response...")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=150,
        messages=conversation
    )

    ai_result = completion.choices[0].message.content
    print(completion.choices[0].message.content)
    return ai_result


def start_robot_conversation(robot_a_context: str, robot_b_context: str, rounds: int, voice_api: str):
    robot_conversation_a = [
        {"role": "system", "content": robot_a_context},
        {"role": "user", "content": f"I am {robot_a_context} and I appear in front of you"}
    ]
    robot_conversation_b = [
        {"role": "system", "content": robot_b_context},
        {"role": "user", "content": f"I am {robot_b_context} and I appear in front of you"}
    ]

    for i in range(rounds):
        print(f"Interaction: {i}")
        # From robot A to robot B
        robot_a_response = get_ai_response(robot_conversation_a)
        robot_conversation_a.append({"role": "assistant", "content": robot_a_response})
        robot_conversation_b.append({"role": "user", "content": robot_a_response})
        # Using boring voice for now ElevenLabs is expensive, but you can use if if you want just uncomment your choice
        # ElevenLabsVoice.better_voice(robot_a_response, default_voice, voice_api)
        boringVoice.speak_text(robot_a_response)

        # From robot B to robot A
        robot_b_response = get_ai_response(robot_conversation_b)
        robot_conversation_b.append({"role": "assistant", "content": robot_b_response})
        robot_conversation_a.append({"role": "user", "content": robot_b_response})
        # Using boring voice for now ElevenLabs is expensive, but you can use if if you want just uncomment your choice
        # ElevenLabsVoice.better_voice(robot_b_response, default_voice, voice_api)
        boringVoice.speak_text(robot_b_response)
