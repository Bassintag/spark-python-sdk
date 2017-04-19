#
#  Client for spark-python-sdk
#  Started on 18/04/2017 by Antoine
#

import requests
import uuid
import json

from AccessTokenRequest import AccessTokenRequest
from AccessTokenResponse import AccessTokenResponse
from NotAuthenticatedError import NotAuthenticatedError
from SparkError import SparkError


class Client:
    TRACKING_ID = "TrackingID"
    ISO8601_FORMAT = "yyyy-MM-dd'T'HH:mm;ss.SSS'Z'"

    def __init__(self,
                 base_uri,
                 auth_code,
                 redirect_uri,
                 access_token,
                 refresh_token,
                 client_id,
                 client_secret,
                 logger):
        self._base_uri = base_uri
        self._auth_code = auth_code
        self._redirect_uri = redirect_uri
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._logger = logger

    def post(self, clazz, path, body):
        return self.read_json(clazz, json.loads(self.request("POST", path, None, body).text))

    def put(self, clazz, path, body):
        return self.read_json(clazz, json.loads(self.request("PUT", path, None, body).text))

    def get(self, clazz, path, params):
        return self.read_json(clazz, json.loads(self.request("GET", path, params, None).text))

    def list(self, clazz, url):
        return Client.PagingIterator(clazz, url, self)

    def list2(self, clazz, path, params):
        return Client.PagingIterator(clazz, self.get_url(path, params), self)

    def delete(self, url):
        headers = self.get_headers()
        response = requests.delete(url, headers=headers)
        Client.check_for_error_response(response, response.status_code)

    def delete2(self, path):
        self.delete(self.get_url(path, None))

    def request(self, method, path, params, body):
        url = self.get_url(path, params)
        return self.request2(url, method, body)

    def request2(self, url, method, body):
        if self._access_token is None:
            if not self.authenticate():
                raise NotAuthenticatedError()
        try:
            return self.do_request(url, method, body)
        except NotAuthenticatedError:
            if self.authenticate():
                return self.do_request(url, method, body)
            else:
                raise

    def authenticate(self):
        if self._client_id is not None and self._client_secret is not None:
            if self._auth_code is not None and self._redirect_uri is not None:
                url = self.get_url("/access_token", None)
                body = AccessTokenRequest()
                body.grant_type = "authorization_code"
                body.client_id = self._client_id
                body.client_secret = self._client_secret
                body.code = self._auth_code
                body.redirect_uri = self._redirect_uri
                response = self.do_request(url, "POST", body)
                response_body = Client.read_json(AccessTokenResponse, response.text)
                self._access_token = response_body.access_token
                self._refresh_token = response_body.refresh_token
                self._auth_code = None
                return True
            else:
                url = self.get_url("/access_token", None)
                body = AccessTokenRequest()
                body.client_id = self._client_id
                body.client_secret = self._client_secret
                body.refresh_token = self._refresh_token
                body.grant_type = "refresh_token"
                response = self.do_request(url, "POST", body)
                response_body = Client.read_json(AccessTokenResponse, response.text)
                self._access_token = response_body.access_token
                return True
        return False

    def do_request(self, url, method, body):
        headers = self.get_headers()
        tracking_id = headers[Client.TRACKING_ID]
        func = None
        if method == "POST":
            func = requests.post
        elif method == "PUT":
            func = requests.put
        elif method == "GET":
            func = requests.get
        if func is None:
            raise SparkError("Invalid request method: %s" % method)
        json_object = None
        if body is not None:
            json_object = Client.write_json(body)
        print("Executing request: url=%s, method=%s, headers=%s, body=%s, trackingID=%s" %
              (url, method, headers, json_object, tracking_id))
        response = func(url, json=json_object, headers=headers, data=json_object)
        Client.check_for_error_response(response, response.status_code)
        return response

    def get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self._access_token is not None:
            authorization = self._access_token
            if not authorization.startswith("Bearer "):
                authorization = "Bearer " + authorization
            headers["Authorization"] = authorization
        headers[Client.TRACKING_ID] = str(uuid.uuid4())
        return headers

    @staticmethod
    def check_for_error_response(connection, response_code):
        if response_code == 401:
            raise NotAuthenticatedError()
        elif response_code < 200 or response_code >= 400:
            error_message_builder = "bad response code "
            error_message_builder += str(response_code)
            response_message = connection.text
            if response_message is not None:
                error_message_builder += " " + response_message
            raise SparkError(error_message_builder)

    def get_url(self, path, params):
        url_string_builder = self._base_uri + path
        if params is not None:
            url_string_builder += "?"
            for param in params:
                url_string_builder += Client.encode(param[0]) + "=" + Client.encode(param[1]) + "&"
        return url_string_builder

    @staticmethod
    def encode(value):
        return str(str(value).encode("utf8"))

    @staticmethod
    def read_json(clazz, parser):
        result = clazz()
        for field in parser:
            setattr(result, field, parser[field])
        return result

    @staticmethod
    def write_json(body):
        v = vars(body)
        return json.dumps(dict((k, v[k]) for k in v if v[k] is not None))

    class PagingIterator:
        def __init__(self, clazz, url, client):
            self._clazz = clazz
            self._url = url
            self._current = None
            self._current_id = None
            self._parser = None
            self._client = client

        def has_next(self):
            if self._parser is None:
                self._current_id = 0
                response = self._client.request2(self._url, "GET", None)
                self._parser = json.loads(response.text)
            if self._current_id < len(self._parser["items"]):
                self._current = Client.read_json(self._clazz, self._parser["items"][self._current_id])
            else:
                return False
            self._current_id += 1
            return True

        def __next__(self):
            if self.has_next():
                return self._current
            raise StopIteration
