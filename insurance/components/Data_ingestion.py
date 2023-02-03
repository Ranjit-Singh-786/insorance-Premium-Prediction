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

    def initiate_data_ingestion(self)
