import json 
import requests 
api_key = 'AIzaSyCIhuN-QzoiXor_DUbh3bB6suOE3I4awm4'
url = ('https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze' +    
    '?key=' + api_key)
data_dict = {
    'comment': {'text': 'fuck yeah'},
    'languages': ['en'],
    'requestedAttributes': {'TOXICITY': {}}
}
response = requests.post(url=url, data=json.dumps(data_dict)) 
response_dict = json.loads(response.content) 
print(json.dumps(response_dict, indent=2))

