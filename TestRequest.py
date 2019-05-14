import requests
from requests.auth import HTTPBasicAuth
url = 'https://api.github.com/events'
xml = "<?xml version='1.0' encoding='utf-8'?><test>67</test>"
response = requests.post(url, xml, auth=('user', 'pass'))

print(response.content)
