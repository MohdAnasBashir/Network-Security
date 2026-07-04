from pymongo import MongoClient
# MongoDB Atlas connection string
uri="mongodb+srv://networksecurity:<@password>@cluster0.xlgsmhu.mongodb.net/?appName=Cluster0"
# Create a connection to MongoDB Atlas
client = MongoClient(uri)
# Check whether the connection is successful
try:
    # Send a ping command to the MongoDB server
    client.admin.command("ping")
    # If no error occurs, connection is successful
    print("Connected Successfully!")
# If any error occurs while connecting
except Exception as e:
    print(e)