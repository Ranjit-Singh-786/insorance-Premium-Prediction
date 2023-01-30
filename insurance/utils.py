import pandas as pd
import numpy as np
import os, sys
from insurance.config import mongoclient
from insurance.logger import logging
from insurance.exception import InsuranceException

# function to load the data from the mongodb database
def get_data(database:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"gethering the data from the mongodb")
        df = pd.DataFrame(list(mongoclient[database][collection_name].find()))
        logging.info(f"succesfully gethered data from the mongodb")
        SHAPE = df.shape
        COLUMNS = df.columns
        logging.info(f"shape of the Data :- {SHAPE} AND columns are {COLUMNS}")
        # removing the defualt "_id" column which defined by the mongodb
        if '_id' in COLUMNS:
            logging.info(f"removing the _id column from the data")
            df = df.drop(['_id'],axis=1)
            logging.info(f"successfully removed")
        else:
            logging.warning(f"error occured during the _id column removing time")
    except Exception as e:
        logging.warning(f"Data gethering operation failed")
        raise InsuranceException(e,sys)
