import os
import random
import json
import tkinter
from tkinter import messagebox
import urllib.request
from ibm_watson import SpeechToTextV1
import shutil  # Move files
import json
import os


# get anki media path
anki_media_path = os.path.expandvars(r'%APPDATA%\Anki2\用户1\collection.media')

# get current directory
current_dir = os.getcwd()

subFolderPath = [f.path for f in os.scandir(current_dir) if f.is_dir()]

# convert subFolderPath to string
outputFolderPath = " ".join(subFolderPath)  # all files contained in this folder which is output from Aboboo

allFileOutput = os.listdir(outputFolderPath)


speech_to_text = SpeechToTextV1(
    iam_apikey='Evul-eCb4QAR7xCS2JlbsaHNhrR4xbiLgTqEZn0oDD_c',
    url='https://stream.watsonplatform.net/speech-to-text/api'
)





# Invoke Ankiconnet
def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']


#########################################
############# Main Body #################
#########################################

# 从0-9中选择8个随机且独立的元素；返回的是字符串
random_number_10 = ''.join(str(x) for x in random.sample(range(0, 9), 8))

for single_audio_name in allFileOutput:
    
    random_number_10 = int(random_number_10) + 1

    key_numbers = str(random_number_10)

    current_audio_path = outputFolderPath + "\\" + single_audio_name

    with open(current_audio_path, 'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            model="de-DE_BroadbandModel",
            audio=audio_file,
            content_type='audio/mp3',
        ).get_result()

    """
    Allowable model values: 
    [
    de-DE_BroadbandModel,    German
    de-DE_NarrowbandModel,   German
    en-GB_BroadbandModel,    English (United Kingdon)
    en-GB_NarrowbandModel,   English (United Kingdon)
    en-US_BroadbandModel,    English (United States)
    en-US_NarrowbandModel,   English (United States)
    en-US_ShortForm_NarrowbandModel,  English (United States)
    fr-FR_BroadbandModel,    French
    fr-FR_NarrowbandModel,   French
    ja-JP_BroadbandModel,    Japanese
    ja-JP_NarrowbandModel,   Japanese
    ko-KR_BroadbandModel,    Korean
    ko-KR_NarrowbandModel,   Korean
    zh-CN_BroadbandModel,    Chinese (Mandarin)
    zh-CN_NarrowbandModel    Chinese (Mandarin)
    ]

    Default: en-US_BroadbandModel
    """
    # 识别后的文本
    # speech_recognition_results = {'results': [{'alternatives': [{'confidence': 0.8, 'transcript': "all of my bill binaries in one place because that's usually "}], 'final': True}], 'result_index': 0}
    # 
    # print(results['results'][0]['alternatives'][0]['transcript'])
    #
    # all of my bill binaries in one place because that's usually
    
    recognition_transcript = speech_recognition_results['results'][0]['alternatives'][0]['transcript']
    
    # move audio to Anki media folder
    os.rename(current_audio_path, anki_media_path + "\\" + key_numbers + ".mp3")

    # import strings into Anki directly

    front_field = "[sound:" + key_numbers + ".mp3]"
    back_field = recognition_transcript

    note = {'deckName': 'Temporary Station', 'modelName': 'Basic',
                'fields': {'Front': front_field, 'Back': back_field}, 'tags': ['']}

    invoke("addNote", note=note)

    print("Import Successfully: " + recognition_transcript )

shutil.rmtree(outputFolderPath, ignore_errors=True)

tkinter.messagebox.showinfo("Speech To Text",
                            'Congratulations!!!')    




   

