#
#  RequestBuilder for spark-python-sdk
#  Started on 18/04/2017 by Antoine
#


class RequestBuilder:

    def query_param(self, key, value):
        raise NotImplementedError("Abstract Method")

    def path(self, *objects):
        raise NotImplementedError("Abstract Method")

    def url(self, url):
        raise NotImplementedError("Abstract Method")

    def post(self, body):
        raise NotImplementedError("Abstract Method")

    def put(self, body):
        raise NotImplementedError("Abstract Method")

    def get(self, body):
        raise NotImplementedError("Abstract Method")

    def __iter__(self):
        raise NotImplementedError("Abstract Method")

    def paginate(self):
        raise NotImplementedError("Abstract Method")

    def delete(self):
        raise NotImplementedError("Abstract Method")
