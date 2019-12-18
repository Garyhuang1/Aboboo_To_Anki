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

"""
Allowable values: 
[ar-AR_BroadbandModel, 
de-DE_BroadbandModel, 
de-DE_NarrowbandModel, 
en-GB_BroadbandModel, 
en-GB_NarrowbandModel, 
en-US_BroadbandModel, 
en-US_NarrowbandModel, 
en-US_ShortForm_NarrowbandModel, 
es-AR_BroadbandModel, 
es-AR_NarrowbandModel, 
es-ES_BroadbandModel, 
es-ES_NarrowbandModel, 
es-CL_BroadbandModel, 
es-CL_NarrowbandModel, 
es-CO_BroadbandModel, 
es-CO_NarrowbandModel, 
es-MX_BroadbandModel, 
es-MX_NarrowbandModel, 
es-PE_BroadbandModel, 
es-PE_NarrowbandModel, 
fr-FR_BroadbandModel, 
fr-FR_NarrowbandModel, 
ja-JP_BroadbandModel, 
ja-JP_NarrowbandModel, 
ko-KR_BroadbandModel, 
ko-KR_NarrowbandModel, 
pt-BR_BroadbandModel, 
pt-BR_NarrowbandModel, 
zh-CN_BroadbandModel, 
zh-CN_NarrowbandModel]

Default: en-US_BroadbandModel
"""



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
            audio=audio_file,
            content_type='audio/mp3',
        ).get_result()

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




   

