import pandas as pd
import numpy as np
import os, sys
from insurance.config import mongoclient
from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.entity import config_entity
import yaml
import pickle

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

# to save the transform data    
def save_numpy_array_data(file_path:config_entity.DataValidationConfig,array:np.array):
    try:
        logging.info('saving operation started by function')
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        np.save(open(file_path,'wb'),array)
    except Exception as e:
        raise InsuranceException(e, sys)
    

# to load transformed numpy array
def load_transformed_data(file_path:str):
    try:
        logging.info('loading transform data')
        if not os.path.exists(file_path):
            raise Exception(f'file not foud {file_path}')
        with open(file_path,'rb') as file_obj:
            data = np.load(file_obj)
        return data
    except Exception as e:
        raise InsuranceException(e,sys)
    
# to save the preprocess models
def save_object(file_path:str,model_obj:object):
    """"this function will save the model object in pickle
    formate.
    """
    try:
        logging.info(f"saving the preprocess models")
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        pickle.dump(model_obj,open(file_path,'wb'))
        logging.info(f"successfully saved your preprocessing models")
    except Exception as e:
        raise InsuranceException(e,sys)
    

def load_model(file_path:str):

    try:
        logging.info(f"loading the model")
        if not os.path.exists(file_path):
            raise Exception(f"file not found error {file_path}")
        else:
            model_obj = pickle.load(open(file_path,'rb'))
            logging.info(f"successfully load the model")
        return model_obj
    except Exception as e:
        raise InsuranceException(e,sys)

