import os 
import sys
import json
#importing dor env in orrder to acces the database variable
from dotenv import load_dotenv
import pymongo
load_dotenv()
#os.getenv->nmeans get this environment varible thats stored in .env file
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)
#is python packages provides set of ropute certificates
#its commonly used byt python libararies
##to establish secure connection
import certifi
#where() function returns the path to the certificate bundle installed by certifi
ca=certifi.where()
import pandas as pd
import numpy as np
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
##now e need to read the file data and save into json file
    def convertercv_to_json(self,filepath):
        try:
            data=pd.read_csv(filepath)
            #drop the indices
            data.reset_index(drop=True,inplace=True)
            ##create a list of json for every record
            records=list(json.loads(data.T.to_json()).values())

            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,database,collection,records):
        try:
            self.database=database
            #refers to the MongoDB collection where your documents will be stored.
            self.collection=collection
            self.records=records
            ##we also need to create a mongo client to connect to our mongo db
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]

            self.collection.insert_many(self.records)

            return (len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=="__main__":
    File_path="Network_Data/phisingData.csv"

    DATABASE="ANASAI"
    Collection="NetworkData"

    networkobj=NetworkDataExtract()
    records=networkobj.convertercv_to_json(filepath=File_path)
    no_of_records=networkobj.insert_data_mongodb(DATABASE,Collection,records)
    print(no_of_records)

    # data = pd.read_csv(File_path)
    # print(data.head())
    # print(data.shape)