#
#  AccessTokenResponse for spark-python-sdk
#  Started on 19/04/2017 by Antoine
#


class AccessTokenResponse:

    def __init__(self):
        self.access_token = None
        self.expires_in = None
        self.refresh_token = None
        self.refresh_token_expires_in = None
