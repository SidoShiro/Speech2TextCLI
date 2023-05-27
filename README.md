# Transcribe Large Audiofile with Whisper

## Setup

1. Require [Python 3.10](https://www.python.org/downloads/release/python-3100/) and [FFMPEG installed](https://ffmpeg.org/) 
2. [Recommended (why to use venv)](https://towardsdatascience.com/why-you-should-use-a-virtual-environment-for-every-python-project-c17dab3b0fd0) Create venv and enter in venv
    ```sh
    python -m venv venv
    
    # Linux
    . venv/bin/activate
    # Windows
    . venv/Script/activate
    ```
3. Install requirements
    ```sh
    # Make sure the (venv) is flag in the terminal
    pip install -r requirements.txt
    ```
4. Fix ffmpeg install if failures : Uninstall and reinstall ffmpeg-python
    ```
    pip uninstall ffmpeg
    pip uninstall ffmpeg-python

    pip install ffmpeg-python
    ```
   

## Run

> With the venv activated.

Usage:

```sh
python app.py stuff.mp3
```

Result will be stored in stuff_transcribe_result.txt

* [Check the demo](./DEMO.md)

### Run with model param


* Model size for whisper are those : "tiny", "small", "base", "medium", "large"
* The argument for the model is in 2nd
* By default the large model will be used

Run on tiny model:
```
python app.py stuff.mp3 tiny
```

Run on base model:
```
python app.py stuff.py base
```

## Logic

* Moviepy will chunk the mp3 audio file into smaller chunk audio
* The audio chunks are then stored in `./tmp_chunks_audio_speach2text/`
* For each chunk audio (in the right order), execute the whisper model (60 seconds maximum)
* Append all text result
* Write to file result `stuff_transcribe_result.txt`
* Print result to stdout

> Once the process is done, you can clean `tmp_chunks_audio_speach2text/` folder

