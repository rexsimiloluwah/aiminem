import argparse
import queue
import sys
import tempfile
import warnings

import openai
import sounddevice as sd
import soundfile as sf
import torch
import whisper
from decouple import config
from pyfiglet import Figlet
from termcolor import colored

warnings.filterwarnings("ignore")

OPENAI_API_KEY = config("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", type=bool, help="Debug mode", default=False)
parser.add_argument(
    "-g", "--gptmodel", type=str, help="GPT model", default="text-davinci-003"
)
parser.add_argument(
    "-w", "--whispermodel", type=str, help="Whisper model", default="base"
)

args = parser.parse_args()

q = queue.Queue()


def show_header() -> None:
    f = Figlet(font="big")
    print(colored(f.renderText("AIMINEM"), "red"))


def show_instructions() -> None:
    message = """
Hi, I am an AI-powered battle rapper. Follow the instructions below to get started:
   1. Press 'r' to record your bars
   2. Press 'Ctrl+C' to stop recording, and watch me generate the dopest bars
   3. Press 'q' to quit the contest
     """
    print(colored(message, "green"))


def show_exit_message() -> None:
    print(
        colored(
            "Sorry to see you go :(, I hope you return with those fire bars...",
            "red",
        )
    )


def transcribe(filename: str) -> str:
    torch.cuda.is_available()
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    model = whisper.load_model(args.whispermodel, device=DEVICE)

    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    _, probs = model.detect_language(mel)

    if args.debug:
        print(f"Detected language: {max(probs, key=probs.get)}")

    options = whisper.DecodingOptions(language="en", fp16=False)
    result = whisper.decode(model, mel, options)

    if args.debug:
        print(result)

    return result.text


def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


def record_audio():
    try:
        filename = tempfile.NamedTemporaryFile(suffix=".wav")

        # to make sure that the file is opened before recording
        with sf.SoundFile(filename, mode="x", samplerate=44100, channels=1) as file:
            with sd.InputStream(samplerate=44100, channels=1, callback=callback) as _:
                count = 0
                print(
                    colored(
                        "Recording in progress, press Ctrl+C to stop",
                        "blue",
                    ),
                    end="",
                )
                while True:
                    if count > 30:
                        print(".", end="", flush=True)
                        count = 0
                    else:
                        count += 1
                    # write the recording to the buffer
                    file.write(q.get())
    except KeyboardInterrupt:
        if args.debug:
            print(f"\nRecording finished: {filename.name}")
        print("\nwaiting for AI response...")
        transcribed_text = transcribe(filename.name)
        print(f"{colored('(You):','green')} {transcribed_text}\n")
        generated_response = generate_response(transcribed_text)
        print(f"{colored('(AI):','yellow')} {generated_response.strip()}\n")
    except Exception as e:
        raise e


def generate_response(text: str):
    response = openai.Completion.create(
        model=args.gptmodel,
        prompt=f"generate a battle rap response to: {text}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def main():
    prompt = input(colored("Enter key: ", "grey"))
    if prompt == "r":
        record_audio()
    if prompt == "q":
        show_exit_message()
        sys.exit(0)


if __name__ == "__main__":
    show_header()
    show_instructions()
    while True:
        main()
