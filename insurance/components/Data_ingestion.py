# in this file we will writte the code. to get the data and split into training ,
# testing, and validation data. after that we will store all the data. into artifact directory.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from insurance.exception import InsuranceException
from insurance.logger import logging
import os,sys
from insurance.entity import config_entity
from insurance.entity import artifact_entity
from insurance import utils

class DataIngestion:
    def __init__(self,data_ingestion_dir:config_entity.DataingestionConfig):
        try:
            self.data_ingestion_dir = data_ingestion_dir
        except Exception as e:
            raise InsuranceException(e,sys)    
# function to perform all the data ingestion operation
    def initiate_data_ingestion(self):
        try:
            logging.info('loading data from the mongodb by getd_data method.')
            df:pd.DataFrame = utils.get_data(
                database=self.data_ingestion_dir.database_name,
                collection_name=self.data_ingestion_dir.collection_name)
            logging.info('data fetched')
            size_of_the_data = df.shape
            logging.info(f'shape of the data {size_of_the_data}')
        
            # to handle the missing value
            logging.info('replacing na value with np.nan')
            df.replace(to_replace='na',value=np.NAN,inplace=True)
            logging.info('replaced')

            # to save the entire data at one place, "feature_store"
            logging.info('Saving the entire data into the feature store.')
            feature_store = os.path.dirname(self.data_ingestion_dir.feature_store_file_path)
            os.makedirs(feature_store,exist_ok=True) # directory path
            df.to_csv(path_or_buf=self.data_ingestion_dir.feature_store_file_path,index=False,header=True)

            # to split the data
            logging.info('spliting the data into train and test data')
            train_df,test_df = train_test_split(df,test_size=self.data_ingestion_dir.test_size,random_state=2)

            # to store training data & testing data
            logging.info('storing the training and test file.')
            training_data_file_path = os.path.dirname(self.data_ingestion_dir.train_file_path)
            os.makedirs(training_data_file_path, exist_ok=True) 
            train_df.to_csv(path_or_buf = self.data_ingestion_dir.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf = self.data_ingestion_dir.test_file_path,index=False,header=True)
            logging.info('successfully store the files !')
            # to set the output for the dataingestion artifact
            logging.info('set the instance variable for the DataIngestionArtifact !')
            DataIngestionArtifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_dir.feature_store_file_path,
                train_file_path=self.data_ingestion_dir.train_file_path,
                test_file_path=self.data_ingestion_dir.test_file_path
            )
            return DataIngestionArtifact
        except Exception as e:
            raise InsuranceException(e,sys)



        
