import numpy as np
import pandas as pd
import os,sys
from insurance import utils
from insurance.entity import config_entity,artifact_entity
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.predictor import ModelResolver

class ModelPusher:
    def __init__(self,modelpusherconfig:config_entity.ModelPusherConfig,
                 transformationArtifact:artifact_entity.DataTransformationArtifact,
                 modeltrainerArtifact:artifact_entity.ModelTrainerArtifact):
        
        try:
            self.modelpusherconfig = modelpusherconfig
            self.transformationArtifact = transformationArtifact
            self.modeltrainerArtifact = modeltrainerArtifact
            self.model_resolver = ModelResolver()
            logging.info(f"modelpusher constractor var configured")
        except Exception as e:
            raise InsuranceException(e,sys)


    def initiate_Modelpusher(self,)->artifact_entity.ModelPusherArtifact:
        try:
            # we are loading current models
            transformer = utils.load_model(file_path=self.transformationArtifact.transformer_object_path)
            target_encoder = utils.load_model(file_path=self.transformationArtifact.target_encoder_path)
            model = utils.load_model(file_path=self.modeltrainerArtifact.model_file_path)
            
            # saved in artifact --> modelpusherfiles
            utils.save_object(file_path=self.modelpusherconfig.pusher_model_path,model_obj=transformer)
            utils.save_object(file_path=self.modelpusherconfig.pusher_encoder_path,model_obj=target_encoder)
            utils.save_object(file_path=self.modelpusherconfig.pusher_Transform_path,model_obj=model)
            logging.info(f"saved models in artifact -> pusherfiles")

            # get the path to save in saved_models
            transfoermer_path = self.model_resolver.get_latest_save_transfomer_path()
            encoder_path = self.model_resolver.get_latest_save_target_encoder_path()
            model_path = self.model_resolver.get_latest_save_model_path()

            # to save the models in saved_models
            utils.save_object(file_path=transfoermer_path,model_obj=transformer)
            utils.save_object(file_path=encoder_path,model_obj=target_encoder)
            utils.save_object(file_path=model_path,model_obj=model)
            logging.info(f"saved models in saved_models")

            # to return modelPusherArtifact
            modelPusherArtifact = artifact_entity.ModelPusherArtifact(pusher_model_dir=self.modelpusherconfig.pusher_model_dir,
                                                                      saved_model_dir=self.modelpusherconfig.saved_model)
            return modelPusherArtifact

        except Exception as e:
            raise InsuranceException(e,sys)