import os,sys
from insurance.exception import InsuranceException
from insurance.logger import  logging
from datetime import datetime
FILE_NAME = os.getenv('FILE_NAME')
TRAIN_FILE_NAME = os.getenv('TRAIN_FILE_NAME')
TEST_FILE_NAME = os.getenv('TEST_FILE_NAME')
TRANSFORMER_OBJECT_FILE_NAME = os.getenv('TRANSFORMER_OBJECT_FILE_NAME')
TARGET_ENCODER_OBJECT_FILE_NAME = os.getenv('TARGET_ENCODER_OBJECT_FILE_NAME')
MODEL_NAME = os.getenv('MODEL_NAME')

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
            raise InsuranceException(e,sys)
    #function to return all the instance variable as dict
    def to_dict(self,):
        try:
            return self.__dict__
        except Exception as e:
            raise InsuranceException(e,sys)

# configuration all the path for the datavalidation components
class DataValidationConfig:
    def __init__(self,trainingPipelingeConfig:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(trainingPipelingeConfig.artifact_dir,'data_validation')
        self.report_file_path = os.path.join(self.data_validation_dir,'report.yaml')
        self.missing_threshold:float = 0.2
        self.base_df_file_path = os.path.join('insurance.csv')


class DataTransformationConfig:
    def __init__(self,trainingPipelingeConfig:TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(trainingPipelingeConfig.artifact_dir,'DataTransformation')
        self.transformer_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)   #transformer.pkl /// model file path
        self.transformed_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))  # after operation save into  tar format
        self.transformed_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)   #target_encoder.pkl

class ModelTrainerConfig:
    def __init__(self,TrainingPipelineConfig:TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(TrainingPipelineConfig.artifact_dir,'model_trainer')
        self.model_file_path = os.path.join(self.model_trainer_dir,'Trained_model',MODEL_NAME)
        self.expected_accuracy = 0.7
        self.overfiting_threshold = 0.2


class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.change_threshold = 0.01


class ModelPusherConfig:
    # we r defining all the file path of pusher model
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_Pusher_dir  = os.path.join(training_pipeline_config.artifact_dir,'modelPusherFiles')
        self.saved_model = os.path.join('saved_models')
        self.pusher_model_dir = os.path.join(self.model_Pusher_dir,'saved_models')
        self.pusher_model_path = os.path.join(self.pusher_model_dir,MODEL_NAME)
        self.pusher_Transform_path = os.path.join(self.pusher_model_dir,TRANSFORMER_OBJECT_FILE_NAME)
        self.pusher_encoder_path = os.path.join(self.pusher_model_dir,TARGET_ENCODER_OBJECT_FILE_NAME)
