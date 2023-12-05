import requests
import json

api_key = 'YOUR_API_KEY'

search_query = 'OpenAI'

endpoint = 'https://api.bing.microsoft.com/v7.0/search'
headers = {'Ocp-Apim-Subscription-Key': api_key}
params = {'q': search_query, 'responseFilter': 'Webpages'}

response = requests.get(endpoint, headers=headers, params=params)
response.raise_for_status()

search_results = response.json()

for webpage in search_results['webPages']['value']:
    print("Title: {}, URL: {}".format(webpage['name'], webpage['url']))
