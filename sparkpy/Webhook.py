#
#  Webhook for spark-python-sdk
#  Started on 19/04/2017 by Antoine
#


class Webhook:

    def __init__(self):
        self.id = None
        self.name = None
        self.ressource = None
        self.event = None
        self.filter = None
        self.targetUrl = None
        self.created = None
