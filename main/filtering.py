import json 
import requests 
api_key = 'AIzaSyCIhuN-QzoiXor_DUbh3bB6suOE3I4awm4'
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
    '?key=' + api_key)

def content_check(text):
    #text = input('what text u want to check ??');
    data_dict = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {},'INSULT': {},
              'THREAT': {}}
    }
    response = requests.post(url=url, data=json.dumps(data_dict))
    response_dict = json.loads(response.content)
    threat_percentage = response_dict['attributeScores']['THREAT']['spanScores'][0]['score']['value'] *100
    insult_percentage = response_dict['attributeScores']['INSULT']['spanScores'][0]['score']['value'] *100
    toxicity_percentage = response_dict['attributeScores']['TOXICITY']['spanScores'][0]['score']['value'] *100
    if threat_percentage>80:
        return "Your content has been classified as threatening, and cannot be posted"
    if insult_percentage>80:
        return "Your content has been classified as insulting, and cannot be posted"
    if toxicity_percentage>80:
        return "Your content has been classified as toxic, and cannot be posted"
    return 0

