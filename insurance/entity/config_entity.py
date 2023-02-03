import os,sys
from insurance.exception import InsuranceException
from insurance.logger import  logging
from datetime import datetime
FILE_NAME = os.getenv('FILE_NAME')
TRAIN_FILE_NAME = os.getenv('TRAIN_FILE_NAME')
TEST_FILE_NAME = os.getenv('TEST_FILE_NAME')

class TrainingPipelineConfig:
    def __init__(self):
        try:
            logging.info('artifact_dir path configuring !')
            self.artifact_dir = os.path.join(os.getcwd(),'artifacts',f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise InsuranceException(e,sys)

class DataingestionConfig:
    # define all the instance variable with the path
    def __init__(self,Training_pipeline_config:TrainingPipelineConfig):  # there we will pass the object of TrainingPiplineConfig class
        try:
            logging.info('configuring all the dataIngestion path variable')
            self.database_name = os.getenv('DATA_BASE_NAME')
            self.collection_name = os.getenv('COLLECTION_NAME')
            self.data_ingestion_dir = os.path.join(Training_pipeline_config.artifact_dir,'data_ingestion')
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,'feature_store')
            self.train_file_path = os.path.join(self.data_ingestion_dir,'dataset',TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,'dataset',TEST_FILE_NAME)
            self.test_size = 0.2
            logging.info('successfully configured')
        except Exception as e:
            logging.error("something went wrong !")
            raise InsuranceException(e,sys)
    #function to return all the instance variable as dict
    def to_dict(self,):
        try:
            return self.__dict__
        except Exception as e:
            raise InsuranceException(e,sys)

