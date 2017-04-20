#
#  LinkedResponse for spark-python-sdk
#  Started on 20/04/2017 by Antoine
#

import re

from Client import Client
from SparkError import SparkError


class LinkedResponse:

    LINK_PATTERN = re.compile(r"\\s*<(\\S+)>\\s*;\\s*rel=\"(\\S+)\",?")

    def __init__(self, client: Client, url, body_creator):
        self._client = client
        self._body_creator = body_creator
        self._response = None
        self._urls = {}
        self.follow_url(url)

    def follow_url(self, url):
        self._response = self._client.request2(url, "GET", None)
        response_code = self._response.status_code
        if not LinkedResponse.is_ok(response_code):
            raise SparkError()
        self.parse_links(self._response)

    def parse_links(self, response):
        self._urls = {}
        link = response.headers.get("Link", None)
        if link is not None and len(link):
            matcher = LinkedResponse.LINK_PATTERN.finditer(link)
            for match in matcher:
                url = match.group(1)
                found_rel = match.group(2)
                self._urls[found_rel] = url

    def get_links(self):
        return self._urls.keys()

    def has_link(self, rel):
        return self._urls.get(rel) is not None

    def consume_body(self):
        return self._body_creator(self._response.text())

    def follow_link(self, rel):
        if self.has_link(rel):
            self.follow_url(self._urls.get(rel))
        else:
            raise SparkError("No element '%s' in urls" % rel)

    def get_link(self, rel):
        return self._urls.get(rel)

    @staticmethod
    def is_ok(response_code):
        return 200 <= response_code < 400
