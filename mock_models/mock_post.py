import requests
dictToSend = {'text': 'my name is ayush', 'from_language': 'en', 'to_language': 'hi'}
res = requests.post('http://localhost:5000/tests/endpoint', json=dictToSend)
print(res.text)
# dictFromServer = res.json()