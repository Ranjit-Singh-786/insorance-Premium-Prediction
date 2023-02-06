from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.utils import get_data
from insurance.entity import config_entity,artifact_entity
from insurance.components.Data_ingestion import DataIngestion
from insurance.components.Data_validation import DataValidation
from insurance.components.Data_transformation import DataTransFormation
from insurance.components.model_trainer import ModelTrainer

import os, sys

#code for testing the logger and exception file
# def log_except_tester():
#     try:
#         logging.info('enter in try blok of log_except_tester fun in main.py.')
#         test = 10/0
#         logging.info('executed try blok in log_except_tester fun in main.py.')
#     except Exception as e:
#         logging.info('error occured in log_except_tester fun in main.py')
#         obj = InsuranceException(e,sys)
#         logging.warning(obj.error_message)
#         logging.info('exception file successfully executed !')

# if __name__ == "__main__":
#     try:
#         logging.info('calling the function')
#         log_except_tester()
#     except Exception as e:
#         print(e)

# code for test the data loader

# DATA_BASE_NAME = "insoranceDB"
# COLLECTION_NAME  = "insoranceCL"
# if __name__=="__main__":
#     try:
#         logging.info(f"start the data gathering process")
#         get_data(DATA_BASE_NAME,COLLECTION_NAME )
#     except Exception as e:
#         logging.warning(f"data gathering operation failed")
#         raise InsuranceException(e,sys)

# code for test all the path
if __name__ == "__main__":
    try:        
        obj_of_training_pipl = config_entity.TrainingPipelineConfig()
        obj_of_dataingestion_config = config_entity.DataingestionConfig(
            Training_pipeline_config=obj_of_training_pipl)
    
        dataIngestion_object = DataIngestion(data_ingestion_dir=obj_of_dataingestion_config)
        # logging.info('calling the dataingestion method')
        retrn_obj_of_dataingestionArtifact = dataIngestion_object.initiate_data_ingestion()

        datavalidation_config_obj = config_entity.DataValidationConfig(trainingPipelingeConfig = obj_of_training_pipl)
        obj_of_data_validation = DataValidation(datavalidationconfig=datavalidation_config_obj,
                                                dataingestionArtifact = retrn_obj_of_dataingestionArtifact)
        data_validation_artifact = obj_of_data_validation.initiate_data_validation()
        obj_of_datatransformationConfig = config_entity.DataTransformationConfig(trainingPipelingeConfig=obj_of_training_pipl)
        obj_of_datatransformation = DataTransFormation(datatrasnformartion=obj_of_datatransformationConfig,
                                                       dataingestionArtifact=retrn_obj_of_dataingestionArtifact)
        obj_of_datatrasnformation_Artifact = obj_of_datatransformation.initiate_data_transformation()

        obj_of_modeltrainerConfig = config_entity.ModelTrainerConfig(TrainingPipelineConfig=obj_of_training_pipl)
        obj_of_modelTrainer = ModelTrainer(modeltrainerconfig=obj_of_modeltrainerConfig,
                                           datatransformationArtifact=obj_of_datatrasnformation_Artifact)
        
        obj_of_modelTrainerArtifact = obj_of_modelTrainer.initiate_modelTrainer()
    except Exception as e:
        raise InsuranceException(e,sys)





