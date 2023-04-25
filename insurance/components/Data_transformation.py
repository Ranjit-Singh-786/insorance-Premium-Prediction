import numpy as np
import pandas as pd
import os,sys
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from insurance.exception import InsuranceException
from insurance import utils
from insurance.logger import logging
from insurance.entity import config_entity,artifact_entity
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
# it is imported to scale the outliers.
from sklearn.preprocessing import RobustScaler   
#from imblearn.combine import SMOTE




class DataTransFormation:
    def __init__(self,
                 datatrasnformartion:config_entity.DataTransformationConfig,
                 dataingestionArtifact:artifact_entity.DataIngestionArtifact):
        try:
            self.datatrasnformartion = datatrasnformartion
            self.dataingestionArtifact = dataingestionArtifact
        except Exception as e:
            raise InsuranceException(e,sys)
        
    
    @classmethod
    def imputer_and_scaler(cls)->Pipeline: # Create cls class
        try:
            simple_imputer_obj = SimpleImputer(strategy='constant', fill_value=0)
            robust_scaler_obj =  RobustScaler()
            # declare a both operation in pipeline
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer_obj),
                    ('RobustScaler',robust_scaler_obj)
                ])
            return pipeline
        except Exception as e:
            raise InsuranceException(e, sys)
        

    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
            try:
                logging.info(f"loading the data in datatransformation file.")
                train_df = pd.read_csv(self.dataingestionArtifact.train_file_path)
                test_df = pd.read_csv(self.dataingestionArtifact.test_file_path)
                
                logging.info(f"removing the target column from test and train data")
                input_feature_train_df=train_df.drop(os.getenv('TARGET_COLUMN'),axis=1)
                input_feature_test_df=test_df.drop(os.getenv('TARGET_COLUMN'),axis=1)

                logging.info(f"declaring target column from train and test data")
                target_feature_train_df = train_df[os.getenv('TARGET_COLUMN')]
                target_feature_test_df = test_df[os.getenv('TARGET_COLUMN')]

                
                # squeeze the target column. it will not do nothing on my target data
                target_feature_train_arr = target_feature_train_df.squeeze()
                target_feature_test_arr = target_feature_test_df.squeeze()

                # to deal with categorical columns
                label_encoder_obj = LabelEncoder()
                logging.info(f"shape of the data before labelencoded :- {input_feature_train_df.shape}")
                logging.info(f"{input_feature_train_df[0]}")
                for col in input_feature_train_df.columns:
                    if input_feature_test_df[col].dtypes == 'O':
                        input_feature_train_df[col] = label_encoder_obj.fit_transform(input_feature_train_df[col])
                        input_feature_test_df[col] = label_encoder_obj.fit_transform(input_feature_test_df[col])
                    else:
                        # else do nothing
                        input_feature_train_df[col] = input_feature_train_df[col]
                        input_feature_test_df[col] = input_feature_test_df[col]
                logging.info(f"after label encoded data shape :- {input_feature_train_df.shape}")

                # to deal with numerical columns
                transformation_pipleine = DataTransFormation.imputer_and_scaler()
                # fitting the pipeline on training data without target columns
                transformation_pipleine.fit(input_feature_train_df)
                # transorm the pipeline objects on training & testing data without target columns
                logging.info(f"performing imputer and Robust scaler on the train & test data")
                input_feature_train_arr = transformation_pipleine.transform(input_feature_train_df)
                input_feature_test_arr = transformation_pipleine.transform(input_feature_test_df)
                
                # preparing the final data as a np.array bcz save_np function wants to np.array format data
                logging.info(f"preparing the final transform data with target column")
                train_arr = np.c_[input_feature_train_arr, target_feature_train_arr ]
                test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]

                # calling the function to save the training and testing transform data
                logging.info('saving the transform training and testing data')
                utils.save_numpy_array_data(file_path=self.datatrasnformartion.transformed_train_path,
                                            array=train_arr)
                utils.save_numpy_array_data(file_path=self.datatrasnformartion.transformed_test_path,
                                            array=test_arr)
                logging.info(f"successfully saved the transform training and testing data")

                # saving the preprocess models
                logging.info(f"saving the preprocess models")
                utils.save_object(file_path=self.datatrasnformartion.transformer_object_path,
                                  model_obj=transformation_pipleine)

                utils.save_object(file_path=self.datatrasnformartion.target_encoder_path,model_obj=label_encoder_obj)

                # datatransformationArtifact object initialization to further proceed
                data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                    transformer_object_path=self.datatrasnformartion.transformer_object_path,
                    transformed_train_path = self.datatrasnformartion.transformed_train_path,
                    transformed_test_path = self.datatrasnformartion.transformed_test_path,
                    target_encoder_path = self.datatrasnformartion.target_encoder_path
                )
                return data_transformation_artifact
            except Exception as e:

                raise InsuranceException(e, sys)

