import platform
import re
import subprocess
import sys

import gradio as gr
import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are a battle rapper"},
]


def transcribe(audio):
    global messages
    audio_file = open(audio, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    messages.append(
        {
            "role": "user",
            "content": f"generate a battle rap response to {transcript['text']}",
        }
    )
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    system_message = response["choices"][0]["message"]
    messages.append({"role": "assistant", "content": system_message})
    print(messages)
    chat_transcript = ""
    for message in messages:
        if message["role"] == "system":
            chat_transcript += message["role"] + ": " + message["content"] + "\n\n"

    output_text = "\n".join(
        list(map(lambda x: x.replace("/", ""), system_message["content"].split("\n")))
    )

    if re.match("linux", sys.platform):
        subprocess.call(["espeak", output_text])
    elif re.match("darwin", sys.platform):
        subprocess.call(["say", output_text])
    else:
        pass

    return f"AIMINEM: {output_text}"


if __name__ == "__main__":
    demo = gr.Interface(
        fn=transcribe,
        inputs=gr.Audio(source="microphone", type="filepath"),
        outputs="text",
    )
    demo.launch()
