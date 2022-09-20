from urllib import response
import requests, uuid, json
from flask import Flask, request
from flask_cors import CORS, cross_origin
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

TEXT_KEY = os.getenv('TEXT_KEY')
SPEECH_KEY = os.getenv('SPEECH_KEY')

def text2text(text, from_language, to_language):
    key = TEXT_KEY
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    location = "westus2"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': to_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request_response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request_response.json()
    translated_text = response[0]['translations'][0]['text']
    return translated_text



@app.route('/text2text', methods=['POST'])
@cross_origin()
def text2text_post():
    text = request.form['text']
    from_language = request.form['from_language']
    to_language = request.form['to_language']

    key = TEXT_KEY
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    location = "westus2"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': to_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    request_response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request_response.json()
    translated_text = response[0]['translations'][0]['text']
    return translated_text


@app.route('/text2speech', methods=['POST'])
@cross_origin()
def text2speech_post():
    text = request.form['text']
    speech_key, service_region = SPEECH_KEY, 'westus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)

    speech_config.speech_synthesis_voice_name='hi-IN-MadhurNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    return speech_synthesis_result.audio_data


@app.route('/speech2text', methods=['POST'])
@cross_origin()
def speech2text_post():
    # text = request.form['text']
    speech_key, service_region = SPEECH_KEY, 'westus'
    audio_input = speechsdk.AudioConfig(filename="Conference.wav")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    return result.text


@app.route('/speech2speech', methods=['POST'])
@cross_origin()
def speech2speech_post():
    # text = request.form['text']
    speech_key, service_region = SPEECH_KEY, 'westus'
    audio_input = speechsdk.AudioConfig(filename="Conference.wav")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    result = speech_recognizer.recognize_once_async().get()
    text = result.text
    text_translated = text2text(text, 'en', 'hi')
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    speech_config.speech_synthesis_voice_name='hi-IN-MadhurNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text_translated).get()
    return speech_synthesis_result.audio_data


if __name__ == '__main__':
    app.run(debug=True)

