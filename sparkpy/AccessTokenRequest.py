#
#  AccessTokenRequest for spark-python-sdk
#  Started on 18/04/2017 by Antoine
#


class AccessTokenRequest:
    def __init__(self):
        self.grant_type = None
        self.client_id = None
        self.client_secret = None
        self.code = None
        self.refresh_token = None
        self.redirect_uri = None
