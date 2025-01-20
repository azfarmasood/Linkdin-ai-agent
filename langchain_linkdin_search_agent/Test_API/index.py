import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.environ["PROXY_API_KEY"]

headers = {"Authorization": "Bearer " + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
     'linkedin_profile_url': 'https://linkedin.com/in/johnrmarty/',
}

response = requests.get(api_endpoint, params = params, headers = headers)

# Check the JSON response
# print(response.json())
# print(response._content)

gist_response = requests.get(
    "https://gist.githubusercontent.com/azfarmasood/0e346101ec0558f87e66a537c162d8f2/raw/04a2fbf0cf2627dc8f45cc933503ec8b1122e090/azfar-masood-json"
)
# print(gist_response.json())
print(response.json())
