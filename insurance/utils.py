import pandas as pd
import numpy as np
import os, sys
from insurance.config import mongoclient
from insurance.logger import logging
from insurance.exception import InsuranceException
import yaml

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
        return df
    except Exception as e:
        raise InsuranceException(e,sys)

# function to write content information in .yaml file
def write_yaml_file(file_path:str,data:dict):
    try:
        file_dir = os.path.dirname(file_path) # fetch the directories path from path
        os.makedirs(file_dir,exist_ok=True)  # created directories
        logging.info('writing roport.yaml file')
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise InsuranceException(e,sys)

# function to convert all numeric columns into float
def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                if df[column].dtypes != 'O':
                    logging.info(f"converting the dtypes")
                    df[column]=df[column].astype('float')
                    logging.info(f"successfully converted the dtypes")
        return df
    except Exception as e:
        raise InsuranceException(e,sys)
