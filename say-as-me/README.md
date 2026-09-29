# say-as-me

Speak a script in your own cloned voice, using Qwen3-TTS on Replicate.

## Installation

```sh
npx skills add https://github.com/RichardBray/skills --skill say-as-me
```

You need [uv](https://docs.astral.sh/uv/), `ffmpeg`, and a `REPLICATE_API_TOKEN` with credit on the account.

## Set up your voice

The skill never stores a voice sample in this repo. Keep yours private in `~/.config/voice-clone/`:

- `reference.wav`: 20-30 seconds of you speaking naturally, in a quiet room, ideally starting and ending on sentence boundaries.
- `reference.txt`: the exact words spoken in that clip, punctuation included. Whisper transcripts often misspell product names, so check it.

Qwen re-reads this clip on every call, so a cleaner or more expressive clip improves every future take.

## Usage

```
/say-as-me [text or script path]
```

Or run the script directly:

```sh
uv run say-as-me/scripts/say.py "Some text to say" out.wav
uv run say-as-me/scripts/say.py @script.txt out.wav --style "Speak at a relaxed, natural conversational pace" --speed 0.92
```

Long text is split into sentence chunks and joined. It prints the duration and words per second so you can catch a rushed take. Qwen tends to read fast; `--speed` slows the finished audio without changing pitch.

Only clone your own voice, and label published videos that use it as synthetic where the platform asks you to.
