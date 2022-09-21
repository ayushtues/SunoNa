from urllib import response
import requests, uuid, json
from flask import Flask, request
from flask_cors import CORS, cross_origin
import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write

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
    # print(body)
    request_response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request_response.json()
    # print(response)
    translated_text = response[0]['translations'][0]['text']
    return translated_text


@app.route('/text2speech', methods=['POST'])
@cross_origin()
def text2speech_post():
    text = request.form['text']
    audio_filename = request.form['audio_filename']
    language = request.form['language']
    speech_key, service_region = SPEECH_KEY, 'westus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_filename)
    language_to_speaker = {'en-IN': 'en-IN-PrabhatNeural', 'hi-IN': 'hi-IN-MadhurNeural'}
    speech_config.speech_synthesis_voice_name=language_to_speaker[language]
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return '200'
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        return cancellation_details.reason


@app.route('/speech2text', methods=['POST'])
@cross_origin()
def speech2text_post():
    audio_filename = request.form['audio_filename']
    from_language = request.form['from_language']
    speech_key, service_region = SPEECH_KEY, 'westus'
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language=from_language
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    return result.text


@app.route('/speech2speech', methods=['POST'])
@cross_origin()
def speech2speech_post():
    audio_output_filename = request.form['audio_output_filename']
    from_language = request.form['from']
    to_language = request.form['to']
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_key, service_region = SPEECH_KEY, 'westus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language=from_language
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once_async().get()
    text = result.text
    text_translated = text2text(text, from_language, to_language)
    
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    language_to_speaker = {'en-IN': 'en-IN-PrabhatNeural', 'hi-IN': 'hi-IN-MadhurNeural'}
    speech_config.speech_synthesis_voice_name=language_to_speaker[to_language]
    audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_output_filename)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text_translated).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return text_translated
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        return cancellation_details.reason


if __name__ == '__main__':
    app.run(debug=True)

