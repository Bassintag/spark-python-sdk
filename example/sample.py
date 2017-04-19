#
#  sample for spark-python-sdk
#  Started on 19/04/2017 by Antoine
#

import sparkpy

# To obtain a developer access token, visit http://developer.ciscospark.com
access_token = "<<secret>>"

# Initialize the client
spark = sparkpy.Spark().builder().base_url("https://api.ciscospark.com/v1").access_token(access_token).build()

# List the rooms that I'm in
for room in spark.rooms():
    print(room.title + ", created " + room.created + ": " + room.id)

# Create a new room
room = sparkpy.Room()
room.title = "Hello World"
room = spark.rooms().post(room)

# Post a text message to the room
message = sparkpy.Message()
message.roomId = room.id
message.text = "Hello World"
spark.messages().post(message)

# Create a new team
team = sparkpy.Team()
team.name = "Brand New Team"
team = spark.teams().post(team)
