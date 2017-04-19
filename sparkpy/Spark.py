#
#  Spark for spark-python-sdk
#  Started on 18/04/2017 by Antoine
#

import SparkImpl
from Client import Client


class Spark:

    class Builder:
        def __init__(self):
            self._redirect_uri = None
            self._auth_code = None
            self._access_token = None
            self._refresh_token = None
            self._client_id = None
            self._client_secret = None
            self._logger = None
            self._base_url = Spark.API_URL

        def base_url(self, url):
            self._base_url = url
            return self

        def redirect_uri(self, uri):
            self._redirect_uri = uri
            return self

        def auth_code(self, code):
            self._auth_code = code
            return self

        def access_token(self, access_token):
            self._access_token = access_token
            return self

        def refresh_token(self, refresh_token):
            self._refresh_token = refresh_token
            return self

        def client_id(self, client_id):
            self._client_id = client_id
            return self

        def client_secret(self, client_secret):
            self._client_secret = client_secret
            return self

        def logger(self, logger):
            self._logger = logger
            return self

        def build(self):
            return SparkImpl.SparkImpl(Client(self._base_url,
                                              self._auth_code,
                                              self._redirect_uri,
                                              self._access_token,
                                              self._refresh_token,
                                              self._client_id,
                                              self._client_secret,
                                              self._logger))

    API_URL = "https://api.ciscospark.com/v1"

    def rooms(self):
        raise NotImplementedError("Abstract method")

    def memberships(self):
        raise NotImplementedError("Abstract method")

    def messages(self):
        raise NotImplementedError("Abstract method")

    def people(self):
        raise NotImplementedError("Abstract method")

    def teams(self):
        raise NotImplementedError("Abstract method")

    def team_memberships(self):
        raise NotImplementedError("Abstract method")

    def webhooks(self):
        raise NotImplementedError("Abstract method")

    def organizations(self):
        raise NotImplementedError("Abstract method")

    def licenses(self):
        raise NotImplementedError("Abstract method")

    def roles(self):
        raise NotImplementedError("Abstract method")

    @staticmethod
    def builder():
        return Spark.Builder()
