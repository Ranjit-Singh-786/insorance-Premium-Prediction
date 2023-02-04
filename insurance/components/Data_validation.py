import numpy as np
import pandas as pd
import os,sys
from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.entity import config_entity
from insurance.entity import artifact_entity
from insurance import utils
from insurance import config
from scipy.stats import ks_2samp
from insurance.config import TARGET_COLUMN

class DataValidation:
    def __init__(self,
                 datavalidationconfig:config_entity.DataValidationConfig,
                 dataingestionArtifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"fetching the datavalidationconfig instance variabel")
            self.datavalidationConfig = datavalidationconfig
            self.dataingestionArtifact = dataingestionArtifact
            self.validation_error = dict()
        except Exception as e:
            raise InsuranceException(e,sys)
    def drop_missing_values_columns(self,df:pd.DataFrame,report_key_name:str):
        try:
            logging.info(f"removing all those columns which has missing values > 20%")
            threshold = self.datavalidationConfig.missing_threshold
            null_report = df.isna().sum()/df.shape[0]
            #selecting column name which contains null
            logging.info(f"selecting column name which contains null above to {threshold}")
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"Columns to drop: {list(drop_column_names)}")
            # writing the name of all columns in report.yaml which will be removed.
            self.validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)
            logging.info(f"dropped columns: {list(drop_column_names)}")

            #return None no columns left
            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise InsuranceException(e,sys)
        

    #  to compare the dataset with base dataframe to current dataframe
    def to_compare_exists_columns(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)
                    logging.info(f"{base_column} These columns is not present in your current dataset.")
                    
            if len(missing_columns)>0:
                # writing the details of all those columns which are missing in our current dataset
                self.validation_error[report_key_name]=missing_columns
                return False
            return True
        except Exception as e:
            raise InsuranceException(e,sys)
            
# to check the samp distribution. and write all the information into the report.yaml
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,report_key_name:str):
        try:
            drift_report=dict()

            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]
                
                same_distribution =ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    #then We are accepting null hypothesis
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }
                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }
                    #different distribution
            # writing all the collected information into the report.yaml file
            self.validation_error[report_key_name]=drift_report
        except Exception as e:
            raise InsuranceException(e,sys)

# to initiate all the functions. for the execution. defined this function
    def initiate_data_validation(self)->artifact_entity.DataValidationArtifact:
        try:
            # reading data from the base enviroment
            logging.info(f"Reading base dataframe")
            base_df = pd.read_csv(self.datavalidationConfig.base_df_file_path)
            base_df.replace({"na":np.NAN},inplace=True)
            logging.info(f"Replace na value in base df")

            #base_df has na as null
            logging.info(f"Drop null values colums from base df")
            base_df=self.drop_missing_values_columns(df=base_df,report_key_name="missing_values_within_base_dataset")

            # reading the training data.get the path from the dataingestionartifact class
            logging.info(f"Reading train dataframe")
            train_df = pd.read_csv(self.dataingestionArtifact.train_file_path)
            logging.info(f"Reading test dataframe")
            test_df = pd.read_csv(self.dataingestionArtifact.test_file_path)

            #removing the missing columns from train & test data
            train_df = self.drop_missing_values_columns(df=train_df,report_key_name="missing_values_within_train_dataset")
            test_df = self.drop_missing_values_columns(df=test_df,report_key_name="missing_values_within_test_dataset")
            
            # converting the dtypes of all numeric columns into float
            exclude_columns = [TARGET_COLUMN]
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)


            logging.info(f"Is all required columns present in train df")
            # this function returning True and False "boolean values"
            train_df_columns_status = self.to_compare_exists_columns(base_df=base_df, current_df=train_df,report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Is all required columns present in test df")
            test_df_columns_status = self.to_compare_exists_columns(base_df=base_df, current_df=test_df,report_key_name="missing_columns_within_test_dataset")

            # if both are status True then both condition will be execute
            # and perform the data_drift operation,means check the samp distribution
            if train_df_columns_status:
                logging.info(f"As all column are available in train df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=train_df,report_key_name="data_drift_within_train_dataset")
            if test_df_columns_status:
                logging.info(f"As all column are available in test df hence detecting data drift")
                self.data_drift(base_df=base_df, current_df=test_df,report_key_name="data_drift_within_test_dataset")
          
            #write the report we got many information in the self.validation_erro =dict()
            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.datavalidationConfig.report_file_path,
                                  data=self.validation_error)
            
            #set the report file path to datavalidationArtifact                
            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_path=self.datavalidationConfig.report_file_path)
            logging.info(f"successfully set the report_file_path to the Data validation artifact")
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e,sys)