import os
os.system("pip install git+https://github.com/openai/whisper.git")
import gradio as gr
import whisper
from moviepy.editor import *

# model = whisper.load_model("base", device="cpu")
model = whisper.load_model("medium", device="cpu")
# model = whisper.load_model("large", device="cpu")

import time

temp_folder = "./temp_audio/"

def chunk_any_audio_long(path: str, path_temp_folder: str):
   audio_clip = AudioFileClip(path)
   # length in seconds of the clip
   n = round(audio_clip.duration)
   counter = 0
   start = 0
   audio_clip.close()
   # time interval
   index = 60
   flag_break = False
   while(True):
     audio_clip = AudioFileClip(path)
     # last loop to exit
     if index >= n:
       flag_break = True
       index = n
     # chunking
     temp = audio_clip.subclip(start, index)
     file = temp_folder + f"temp_{counter}.mp3"
     temp.write_audiofile(filename=file)
     temp.close()
     counter += 1
     start = index
     audio_clip.close()
     if flag_break:
         break
     index += 60


def transcribe_from_temp_audio(temp_audio_folder: str):
    files = os.listdir(temp_audio_folder)
    nn_chunks = len(files)
    res = ""
    for i, f in enumerate(files):
        print(f"{i}/{nn_chunks}")
        res += inference_model(temp_audio_folder + '/' + f)
    return res

def inference_model(file_path):
    out = model.transcribe(file_path)
    # print(out)
    return out.get('text', 'N/A')

def main():
    FOLDER_TEMP_AUDIO_CHUNKED = "./temp_audio"

    ENTRETIEN = "Entretien1.mp3"
    CHARLES = "Charles_de_Gaulle_-_Appel_du_22_juin_version_originale.mp3"
    file_result = "transcribe_result.txt"

    print("Start")
    print("File chunking")
    chunk_any_audio_long(ENTRETIEN, temp_folder)
    print("File Transcirption")
    res = transcribe_from_temp_audio(FOLDER_TEMP_AUDIO_CHUNKED)
    print("Result")
    print(res)
    print(f"Result written to {file_result}")
    with open(file_result, "w") as f_write:
        f_write.write(res)
    print("Done")

main()

