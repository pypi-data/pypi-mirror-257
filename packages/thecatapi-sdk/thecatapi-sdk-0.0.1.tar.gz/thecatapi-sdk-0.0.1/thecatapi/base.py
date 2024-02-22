import requests
import json


class Base:
    _BASE_URL = 'https://api.thecatapi.com/v1'

    def __init__(self, api_key, base_url=None):
        self.api_key = api_key
        self._base_url = base_url if base_url else Base._BASE_URL

    def _headers(self):
        return {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

    def _url(self, path):
        """ This method appends the given path to the base url
        :param path:
        :return:
        """
        return self._BASE_URL + path

    def make_request(self, method='GET', path='', data=None, json_data=None, files=None):
        """Handles all incoming requests, returns appropriate response, updates headers and payload
        :param json_data:
        :param method:
        :param path:
        :param data:
        :param files
        :return:
        """
        method_map = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }
        request = method_map.get(method)
        try:
            response = request(path, data=data, headers=Base._headers(self), json=json_data, files=files)
            return response.json()
        except requests.exceptions.ConnectionError:
            return "A connection error occurred. Please check your internet connection."
        except requests.exceptions.Timeout:
            return "The request timed out."
        except requests.exceptions.HTTPError as e:
            return "HTTP Error:", e
        except requests.exceptions.RequestException as e:
            return "An error occurred:", e
