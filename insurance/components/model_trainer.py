from insurance.entity import config_entity,artifact_entity
from insurance.exception import InsuranceException
from insurance.logger import logging
import os,sys
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from insurance import utils

class ModelTrainer:
    def __init__(self,
                 modeltrainerconfig:config_entity.ModelTrainerConfig,
                 datatransformationArtifact:artifact_entity.DataTransformationArtifact):
        
        try:
            self.modeltrainerconfig = modeltrainerconfig
            self.datatransformationArtifact = datatransformationArtifact
        except Exception as e:
            raise InsuranceException(e,sys)
     
    def declared_model(self,x,y):
        try:
            logging.info(f"fitting the model")
            xgr = XGBRegressor()
            xgr.fit(x,y)
            return xgr
        except Exception as e:
            raise InsuranceException(e,sys)
        

    def initiate_modelTrainer(self,):
        # transformed file paths
        try:
            logging.info(f"initiating model training instance method")
            train_df_path = self.datatransformationArtifact.transformed_train_path
            test_df_path = self.datatransformationArtifact.transformed_test_path

            #load the data
            train  = utils.load_transformed_data(train_df_path)
            test  = utils.load_transformed_data(test_df_path)

            # split the data into independent and dependent
            x_train,y_train = train[:,:-1],train[:,-1]
            x_test,y_test = test[:,:-1],test[:,-1]

            model = self.declared_model(x= x_train,y= y_train)
            logging.info(f"model fitted on our dataset")
            logging.info(f"training data sample {x_train[0]} and {y_train[0]}")
            logging.info(f"model training data shape {x_train.shape}")

            logging.info('getting the prediction')
            prediction_on_training_data =  model.predict(x_train)
            train_r2_score = r2_score(y_true=y_train,y_pred=prediction_on_training_data)

            prediction_on_testing_data = model.predict(x_test)
            test_r2_score = r2_score(y_true=y_test,y_pred=prediction_on_testing_data)
            if train_r2_score < self.modeltrainerconfig.expected_accuracy:
                raise Exception(f"training accuracy is low to our expected accuracy {self.modeltrainerconfig.expected_accuracy} model accuracy is :- {train_r2_score}") 
            
            #to check the underfit & overfit condition
            differnce = train_r2_score-test_r2_score
            if differnce > self.modeltrainerconfig.overfiting_threshold:
                raise Exception(f"model is not generalized model.")
            
            # to save the model object
            utils.save_object(file_path=self.modeltrainerconfig.model_file_path , model_obj=model)
            ModelTrainerArtifact = artifact_entity.ModelTrainerArtifact(model_file_path=self.modeltrainerconfig.model_file_path,
                                                                        r2_train_score=train_r2_score,
                                                                        r2_test_score=train_r2_score)
            logging.info(f"your model successfully trained with training accuracy :- {train_r2_score} and testing accuracy :- {test_r2_score}")
            return ModelTrainerArtifact
        except Exception as e:
            raise InsuranceException(e,sys)
        

        

    