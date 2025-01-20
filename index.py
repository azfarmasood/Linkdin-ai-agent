import os
import requests
from dotenv import load_dotenv

load_dotenv()

PROXY_CURL_API_KEY = os.environ['PROXY_API_KEY']


api_key = PROXY_CURL_API_KEY


headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
params = {
    'linkedin_profile_url': 'https://linkedin.com/in/syed-azfar-masood-09697228b/',
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)




gist_response = requests.get("https://gist.githubusercontent.com/azfarmasood/7b6bb4e01000e8c1c505cdb2dc8704a4/raw/bc335b6750af149c946e885d9a8ad902f91d2c41/gistfile1.txt")
