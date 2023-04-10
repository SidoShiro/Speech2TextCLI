#!/bin/python
import os
import sys
import gradio as gr
import whisper
from moviepy.editor import *
import time
import shutil


def chunk_any_audio_long(path: str, path_temp_folder: str):
    """Seperate an audio into chunks of 60 seconds"""
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


def transcribe_from_temp_audio(model: object, path_temp_folder: str):
    """Get transcription of each chunk audio stored in the temp folder, and return a result"""
    files = os.listdir(path_temp_folder)
    # print(files)
    # files are in form : temp_NUMBER.mp3
    # Starting 0
    nn_chunks = len(files)
    res = ""
    for i in range(nn_chunks):
        file_to_process = "temp_" + str(i) + ".mp3"        
        print(f"{i}/{nn_chunks}: {file_to_process}")
        res += inference_model(model, path_temp_folder + "/" + file_to_process) + "\n"
    return res

def inference_model(model: object, file_path: str):
    """Infer the model (Whisper, thanks OpenAI) to transcribe the chunked audio"""
    out = model.transcribe(file_path)
    # print(out)
    return out.get('text', 'N/A')

def main():
    """Entry of the Speech2textCli tool"""
    if len(sys.argv) == 3:
        if sys.argv[2] not in ["tiny", "small", "base", "medium", "large"]:
            print("Model size not recongnize, switching to medium")
            model_size = "medium"
        model_size = sys.argv[2]
    else:
        model_size = "large"
    print("Speech2TextCLI")
    print("==============")
    print(f"Model size set to {model_size}")
    # Size of the model to run, uncomment, recomment when needed
    model = whisper.load_model(model_size, device="cpu")
    source_audio_file = sys.argv[1]
    FOLDER_TEMP_AUDIO_CHUNKED = "./tmp_chunks_audio_speach2text"
    file_result = source_audio_file + "_transcribe_result.txt"
    file_result = file_result.replace(".mp3", "")
    print("Start")
    print("File chunking")
    chunk_any_audio_long(source_audio_file, FOLDER_TEMP_AUDIO_CHUNKED)
    print("File Transcription")
    res = transcribe_from_temp_audio(model, FOLDER_TEMP_AUDIO_CHUNKED)
    print("Result")
    print(res)
    print(f"Result written to {file_result}")
    with open(file_result, "w") as f_write:
        f_write.write(res)
    print("Done")

main()

