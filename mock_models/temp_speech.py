import azure.cognitiveservices.speech as speechsdk


speech_key, service_region = 'cec1f6409e014607be81df883d1474fe', 'westus'
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)

speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
text = input("Enter text: ")

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
stream = speechsdk.AudioDataStream(speech_synthesis_result)

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
    stream.save_to_wav_file("temp.wav")
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")