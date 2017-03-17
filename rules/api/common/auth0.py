import requests
import json


class Auth0(object):
    def __init__(self, token_url, token_info):
        self.token = Auth0.__get_token(token_url, token_info)

    @staticmethod
    def __get_token(token_url, token_info):
        payload = json.dumps(token_info)
        response = requests.post(token_url, data=payload, headers={'Content-Type': 'application/json'})
        return response.json()

    @staticmethod
    def __get_auth_header(token_type, access_token):
        return token_type + ' ' + access_token

    def get_auth_header(self):
        return Auth0.__get_auth_header(self.token['token_type'], self.token['access_token'])

    def authorized_get(self, url):
        response = requests.get(url, headers={'Authorization': self.get_auth_header()})
        return response.json()