#!/bin/python
import os
import sys
os.system("pip install git+https://github.com/openai/whisper.git")
import gradio as gr
import whisper
from moviepy.editor import *
import time
import shutil


# Size of the model to run, uncomment, recomment when needed
# model = whisper.load_model("tiny", device="cpu")
# model = whisper.load_model("base", device="cpu")
# model = whisper.load_model("medium", device="cpu")
model = whisper.load_model("large", device="cpu")


def chunk_any_audio_long(path: str, path_temp_folder: str):
    try:
        shutil.rmtree(path_temp_folder)
    except:
        pass
    os.mkdir(path_temp_folder)
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
        file = path_temp_folder + "/" + f"temp_{counter}.mp3"
        temp.write_audiofile(filename=file)
        temp.close()
        counter += 1
        start = index
        audio_clip.close()
        if flag_break:
            break
        index += 60


def transcribe_from_temp_audio(path_temp_folder: str):
    files = os.listdir(path_temp_folder)
    # print(files)
    # files are in form : temp_NUMBER.mp3
    # Starting 0
    nn_chunks = len(files)
    res = ""
    for i in range(nn_chunks):
        file_to_process = "temp_" + str(i) + ".mp3"        
        print(f"{i}/{nn_chunks}: {file_to_process}")
        res += inference_model(path_temp_folder + "/" + file_to_process) + "\n"
    return res

def inference_model(file_path: str):
    out = model.transcribe(file_path)
    # print(out)
    return out.get('text', 'N/A')

def main():
    FOLDER_TEMP_AUDIO_CHUNKED = "./tmp_chunks_audio_speach2text"
    file_result = sys.argv[1] + "_transcribe_result.txt"

    print("Start")
    print("File chunking")
    chunk_any_audio_long(sys.argv[1], FOLDER_TEMP_AUDIO_CHUNKED)
    print("File Transcirption")
    res = transcribe_from_temp_audio(FOLDER_TEMP_AUDIO_CHUNKED)
    print("Result")
    print(res)
    print(f"Result written to {file_result}")
    with open(file_result, "w") as f_write:
        f_write.write(res)
    print("Done")

main()

