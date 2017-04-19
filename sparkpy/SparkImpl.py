#
#  SparkImpl for spark-python-sdk
#  Started on 18/04/2017 by Antoine
#

from Room import Room
from Membership import Membership
from Message import Message
from Person import Person
from Team import Team
from TeamMembership import TeamMembership
from Webhook import Webhook
from Organization import Organization
from License import License
from Role import Role

from RequestBuilderImpl import RequestBuilderImpl


class SparkImpl():

    def __init__(self, client):
        self._client = client

    def rooms(self):
        return RequestBuilderImpl(Room, self._client, "/rooms")

    def memberships(self):
        return RequestBuilderImpl(Membership, self._client, "/memberships")

    def messages(self):
        return RequestBuilderImpl(Message, self._client, "/messages")

    def people(self):
        return RequestBuilderImpl(Person, self._client, "/people")

    def teams(self):
        return RequestBuilderImpl(Team, self._client, "/teams")

    def team_memberships(self):
        return RequestBuilderImpl(TeamMembership, self._client, "/team/memberships")

    def webhooks(self):
        return RequestBuilderImpl(Webhook, self._client, "/webhooks")

    def organizations(self):
        return RequestBuilderImpl(Organization, self._client, "/organizations")

    def licenses(self):
        return RequestBuilderImpl(License, self._client, "/licenses")

    def roles(self):
        return RequestBuilderImpl(Role, self._client, "/roles")
