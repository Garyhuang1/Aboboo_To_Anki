import os
import random
import json
import tkinter
from tkinter import messagebox
import urllib.request
from ibm_watson import TextToSpeechV1

# set API and URL
text_to_speech = TextToSpeechV1(
    iam_apikey='Q9KsR3ID0t1YEQgvjEqcXLSBeV1OS4q6U5BP8EhYbTY2',
    url='https://stream.watsonplatform.net/text-to-speech/api'
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

################################################################
#######################  Main Body   ###########################
################################################################

# get anki media path
anki_media_path = os.path.expandvars(r'%APPDATA%\Anki2\用户1\collection.media')

# 从0-9中选择8个随机且独立的元素；返回的是字符串
random_number_10 = ''.join(str(x) for x in random.sample(range(0, 9), 8))

with open("raw_texts.txt", "r+", encoding="utf-8") as raw_text:  # 打开单个字幕文本写入Text

    for single_line in raw_text:

        random_number_10 = int(random_number_10) + 1

        #产生单条音频流 / Generate single audio stream  (格式是bits)
        audio_bits = text_to_speech.synthesize(str(single_line),
                                               voice = 'en-US_MichaelV3Voice',
                                               accept = 'audio/mp3').get_result().content  #without '.content', it will return response code !

        key_numbers = str(random_number_10)

        audio_name = key_numbers + "." + "mp3"

        single_anki_audio_path = anki_media_path + "\\" + key_numbers + "." + "mp3"

        # 写入单个音频流到 Anki 媒体文件
        open(single_anki_audio_path, "wb").write(audio_bits)

        # 生成 Anki 正反字段
        front_field = "[sound:" + key_numbers + ".mp3]"
        back_field = str(single_line)

        # import strings into Anki directly
        note = {'deckName': 'Temporary Station', 'modelName': 'Basic',
                'fields': {'Front': front_field, 'Back': back_field}, 'tags': ['']}

        invoke("addNote", note=note)

        print("generate " + key_numbers + ".mp3" + " successfully!!! ")

tkinter.messagebox.showinfo("Text To Speech",
                            'Congratulations!!!')


