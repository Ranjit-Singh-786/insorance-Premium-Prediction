from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.utils import get_data
from insurance.entity import config_entity,artifact_entity
from insurance.components.Data_ingestion import DataIngestion
from insurance.components.Data_validation import DataValidation
from insurance.components.Data_transformation import DataTransFormation
from insurance.components.model_trainer import ModelTrainer
from insurance.components.model_evaluation import ModelEvaluation
from insurance.components.model_pusher import ModelPusher
from insurance.predictor import ModelResolver
import os, sys


def RunTrainingPipeline():          
        try:           
            logging.info(f"Runing The Training pipeline !")
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

            # Model Evaluation
            model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config = obj_of_training_pipl)
            model_eval = ModelEvaluation(model_eval_config = model_eval_config,
                                        data_ingestion_artifact = retrn_obj_of_dataingestionArtifact,
                                        data_transformation_artifact = obj_of_datatrasnformation_Artifact,
                                        model_trainer_artifact = obj_of_modelTrainerArtifact)
            model_evl_artifact = model_eval.intitate_model_evaluation()

            #modelpusher
            modelpusherConfig = config_entity.ModelPusherConfig(training_pipeline_config=obj_of_training_pipl)
            obj_of_model_pusher = ModelPusher(modelpusherconfig=modelpusherConfig,
                                                transformationArtifact=obj_of_datatrasnformation_Artifact,
                                                modeltrainerArtifact=obj_of_modelTrainerArtifact)
            obj_of_modelPusherArtifact = obj_of_model_pusher.initiate_Modelpusher()

        except Exception as e:
            raise InsuranceException(e,sys)