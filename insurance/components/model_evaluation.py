from insurance.entity import artifact_entity,config_entity
from insurance.exception import InsuranceException
from insurance.logger import logging
from typing import Optional
import os,sys 
from insurance.utils import load_model
from sklearn.metrics import r2_score
from sklearn.pipeline import Pipeline
import pandas as pd
from insurance import utils
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from insurance.predictor import ModelResolver
from insurance.config import TARGET_COLUMN


class ModelEvaluation:
    def __init__(self,
                model_eval_config: config_entity.ModelEvaluationConfig,
                data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
                data_transformation_artifact:artifact_entity.DataTransformationArtifact,
                model_trainer_artifact:artifact_entity.ModelTrainerArtifact):


        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_resolver = ModelResolver()
        except Exception as e:
            raise InsuranceException(e, sys)



    def intitate_model_evaluation(self)->artifact_entity.ModelEvaluationArtifact:
        try:
            latest_dir_path = self.model_resolver.get_latest_dir_path()

            if latest_dir_path == None:   # after pusher operation it will not be None
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                # if above condition is true then function will stoped here
                return model_eval_artifact


            # Find location previous model in saved_model
            transfoer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            traget_encoder_path = self.model_resolver.get_latest_target_encoder_path()

            # Previosu model from saved_models dir
            transformer = load_model(file_path=transfoer_path)
            model = load_model(file_path=model_path)
            target_encoder = load_model(file_path=traget_encoder_path)

            # to get the current model
            current_transformer = load_model(file_path=self.data_transformation_artifact.transformer_object_path)
            current_model = load_model(file_path=self.model_trainer_artifact.model_file_path)
            current_target_encoder = load_model(file_path=self.data_transformation_artifact.target_encoder_path)

            # get the transform_test  data. to evaluate both model, saved_model Vs current model
            trasnform_test_data = utils.load_transformed_data(file_path=self.data_transformation_artifact.transformed_test_path)
            
            trasnform_test_data = pd.DataFrame(trasnform_test_data)
            column = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
            trasnform_test_data.columns = column
            input_features_name = os.getenv('INPUT_FEATURE_NAME').split(',')
            target_df = trasnform_test_data[TARGET_COLUMN]
            
            input_arr = trasnform_test_data[input_features_name]
            y_true = target_df
            # previous model testing
            y_pred = model.predict(input_arr)
            previous_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"accuracy of saved_model model on transform test data :- {previous_model_score}")


            # Accuracy of current model

            input_feature_name = list(current_transformer.feature_names_in_)
            y_pred = current_model.predict(input_arr)

            current_model_score = r2_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"accuracy of current model on transform test data :- {current_model_score}")



            # FInal comparision between both model
            if current_model_score <= previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                print("Current model is not better than previous model")
            else:
                print('current model is batter than previous model !')
                logging.info(f"current model is batter than previous model !")

            logging.info(f"evaluated both model on transformed test data")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted =  True, 
            improved_accuracy=current_model_score - previous_model_score)
            logging.info(f"current_model_score - previous_model_score = {current_model_score - previous_model_score}")

            # write the message in log which one is better
            is_good_or_not = current_model_score - previous_model_score
            if is_good_or_not >= self.model_eval_config.change_threshold:
                logging.info(f"current model is good than previous model")
            else:
                logging.info(f"current model is not good to our previous model")

            return model_eval_artifact

        except Exception as e:
            raise InsuranceException(e, sys)