const LANGUAGE_1 = 'en-IN'
const LANGUAGE_2 = 'hi-IN'

function texta2b() {
    var input_text = document.getElementById("TextMessageA").value;
    var dictToSend_text2text = { 'text': input_text, 'from_language': LANGUAGE_1, 'to_language': LANGUAGE_2 }
    var callback = $.ajax({
        type: "POST",
        url: "http://localhost:5000/text2text",
        data: dictToSend_text2text,
        success: function (msg) {
            var b = document.getElementById("ReceiveTextMessageB");
            b.value = msg;
        }
    });
}

function textb2a() {
    var input_text = document.getElementById("TextMessageB").value;
    var dictToSend_text2text = { 'text': input_text, 'from_language': LANGUAGE_2, 'to_language': LANGUAGE_1 }
    var callback = $.ajax({
        type: "POST",
        url: "http://localhost:5000/text2text",
        data: dictToSend_text2text,
        success: function (msg) {
            var a = document.getElementById("ReceiveTextMessageA");
            a.value = msg;
        }
    });
}

function playtextA()
{
    var input_text = document.getElementById("ReceiveTextMessageA").value;
    console.log(input_text);
    var dictToSend_text2speech = { 'text': input_text, 'language': LANGUAGE_1, 'audio_filename': 'text2speech.wav' }
    var callback = $.ajax({
        type: "POST",
        url: "http://localhost:5000/text2speech",
        data: dictToSend_text2speech,
        success: function (msg) {
            console.log(dictToSend_text2speech['audio_filename']);
            var audio = new Audio(dictToSend_text2speech['audio_filename']);
            audio.play();
        }
    });
}

function playtextB()
{
    var input_text = document.getElementById("ReceiveTextMessageB").value;
    console.log(input_text);
    var dictToSend_text2speech = { 'text': input_text, 'language': LANGUAGE_2, 'audio_filename': 'text2speech.wav' }
    var callback = $.ajax({
        type: "POST",
        url: "http://localhost:5000/text2speech",
        data: dictToSend_text2speech,
        success: function (msg) {
            console.log(dictToSend_text2speech['audio_filename']);
            var audio = new Audio(dictToSend_text2speech['audio_filename']);
            audio.play();
        }
    });
}

function recordA(){
    var dictToSend_speech2speech = { 'audio_output_filename': 'speech2speechB.wav', 'from': LANGUAGE_1, 'to': LANGUAGE_2 }
    var callback = $.ajax({
        type: "POST",
        url: "http://localhost:5000/speech2speech",
        data: dictToSend_speech2speech,
        success: function (msg) {
            var x = document.getElementById("ReceiveVoiceMessageB");
            x.value = msg;
        }
    });

}

function recordB(){
    var dictToSend_speech2speech = { 'audio_output_filename': 'speech2speechA.wav', 'from': LANGUAGE_2, 'to': LANGUAGE_1 }
    var callback = $.ajax({
        type: "POST",
        url: "http://localhost:5000/speech2speech",
        data: dictToSend_speech2speech,
        success: function (msg) {
            var x = document.getElementById("ReceiveVoiceMessageA");
            x.value = msg;
        }
    });

}

function playVoiceA()
{
    var audio = new Audio('speech2speechA.wav');
    audio.play();  
}

function playVoiceB()
{
    var audio = new Audio('speech2speechB.wav');
    audio.play();  
}

