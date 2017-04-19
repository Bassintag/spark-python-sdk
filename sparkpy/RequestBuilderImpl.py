#
#  RequestBuilderImpl for spark-python-sdk
#  Started on 18/04/2017 by Antoine
#

from RequestBuilder import RequestBuilder


class RequestBuilderImpl(RequestBuilder):

    def __init__(self, clazz, client, path):
        self._client = client
        self._path_builder = path
        self._params = []
        self._url = None
        self._clazz = clazz

    def query_param(self, key, value):
        self._params.append((key, value))
        return self

    def path(self, *paths):
        for path in paths:
            self._path_builder += path
        return self

    def url(self, url):
        self._url = url
        return self

    def post(self, body):
        if self._url is not None:
            return self._client.post(self._clazz, self._url, body)
        else:
            return self._client.post(self._clazz, self._path_builder, body)

    def put(self, body):
        if self._url is not None:
            return self._client.put(self._clazz, self._url, body)
        else:
            return self._client.put(self._clazz, self._path_builder, body)

    def get(self, body):
        if self._url is not None:
            return self._client.get(self._clazz, self._url)
        else:
            return self._client.get(self._clazz, self._path_builder)

    def __iter__(self):
        if self._url is not None:
            return self._client.list(self._clazz, self._url)
        else:
            return self._client.list2(self._clazz, self._path_builder, self._params)

    def paginate(self):
        if self._url is not None:
            return self._client.paginate(self._url)
        else:
            return self._client.paginate2(self._path_builder, self._params)

    def delete(self):
        if self._url is not None:
            self._client.delete(self._url)
        else:
            self._client.delete(self._path_builder)
