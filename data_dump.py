import pymongo
import pandas as pd
import json
# make the client for mongodb
client = pymongo.MongoClient("mongodb+srv://ranjitSingh:G7GLDHepgyXnsaQM@insorancecluster.yikupch.mongodb.net/?retryWrites=true&w=majority")
DATA_BASE_NAME = "insoranceDB"
COLLECTION_NAME  = "insoranceCL"
FILE_PATH = (r"C:\Users\Ranjit Singh\Desktop\insourance premium prediction\insurance.csv")

if __name__=="__main__":
    df = pd.read_csv(FILE_PATH)
    print(f"Rows and columns: {df.shape}")

    df.reset_index(drop = True, inplace = True)

    json_record = list(json.loads(df.T.to_json()).values())
    print(json_record[0])

    client[DATA_BASE_NAME][COLLECTION_NAME].insert_many(json_record)


