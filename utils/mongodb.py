from motor.motor_asyncio import AsyncIOMotorClient

### Insert your configuration for MongoDB Atlas ###
# user = ''
# password = ''
# host = ''
#
# # MongoDB URI
# URI = 'mongodb+srv://'
# URI += user + ':'
# URI += password
# URI += host
#
# client = AsyncIOMotorClient(URI)

user = 'skku'
password = 'iotlab'
host = '@cluster0.au5ee.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

# MongoDB URI
URI = 'mongodb+srv://'
URI += user + ':'
URI += password
URI += host

client = AsyncIOMotorClient(URI)

