from urllib import response
import requests, uuid, json
from flask import Flask, request
from flask_cors import CORS, cross_origin
import azure.cognitiveservices.speech as speechsdk


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/text2text', methods=['POST'])
@cross_origin()
def text2text():
    text = request.form['text']
    from_language = request.form['from_language']
    to_language = request.form['to_language']

    key = ""
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
def text2speech():
    text = request.form['text']
    speech_key, service_region = 'cec1f6409e014607be81df883d1474fe', 'westus'
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)

    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    return speech_synthesis_result.audio_data


if __name__ == '__main__':
    app.run(debug=True)

