<h1 align="center">
  AIMINEM
</h1>
<h4 align="center">
    An AI-powered battle rapper using OpenAI Whisper and GPT-3 🚀.
</h4>

[![experimental](https://badges.github.io/stability-badges/dist/experimental.svg)](https://github.com/badges/stability-badges)

<a href="https://www.loom.com/share/7e6ba54703f44394bb517e5e2ca6b676">
  <p>AIMINEM DEMO - Watch Video</p>
  <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/7e6ba54703f44394bb517e5e2ca6b676-with-play.gif">
</a>

### Uses

- Python (>3.6)
- [Sounddevice](https://pypi.org/project/sounddevice/): for obtaining the audio recording
- [OpenAI Whisper](https://github.com/openai/whisper): for transcribing the audio recording
- [OpenAI GPT-3](https://pypi.org/project/openai/): for generating a response to the transcribed audio recording

### Requirements

- [ffmpeg](https://ffmpeg.org/download.html)

### How it works?

AIMINEM uses a simple interactive CLI program to record audio from a user, then stores the audio stream in a buffer. This audio stream is transcribed using `Whisper`, then the transcribed text is used to generate a battle rap response using `GPT-3`.

### Usage

1. Clone the repository

```bash
$git clone https://github.com/rexsimiloluwah/aiminem
$cd aiminem
```

2. Create/Initialize a virtual environment using `venv` or `poetry`

- For `venv`

```bash
$python -m venv env
$source env/bin/activate
```

3. Install the dependencies using `pip` or `poetry`

- For `venv`

```bash
$pip install -r requirements.txt
```

- For `poetry`

```bash
$poetry install
```

4. Update the `.env` file with your `OPENAI_API_KEY` as shown in `.env.sample`

```bash
$cp .env.sample .env
#replace <your_openai_api_key>
```

5. Run the CLI and follow the instructions to use AIMINEM

- For `venv`

```bash
$python main.py
```

- For `poetry`

```bash
$poetry run python -m main.py
```

6. Advanced Usage

To view advanced usage instructions:

```bash
$python main.py -h
```

