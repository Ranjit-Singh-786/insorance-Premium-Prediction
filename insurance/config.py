import pymongo
import os,sys
from dataclasses import dataclass
#creating the enviroment class to connect with them mongodb database
@dataclass
class EnviromentVariable:
    # there is :str just typing hints concept which are defining that it will get str value
    mongodb_url:str = os.getenv("MONGODB_URL")
# configure the mongoclient the mongoclient
env_var = EnviromentVariable()
mongoclient = pymongo.MongoClient(env_var.mongodb_url)
TARGET_COLUMN = 'charges'
print(env_var.mongodb_url)