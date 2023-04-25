
from insurance.exception import InsuranceException
from insurance.logger import logging
from insurance.predictor import ModelResolver
import pandas as pd
from insurance import utils
import numpy as np
import os
import sys
from datetime import datetime
from typing import Optional


DATA_BASE_NAME = os.getenv('DATA_BASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

PREDICTION_DIR = "prediction"
default_data_path = r"C:\Users\Ranjit Singh\Desktop\insorance-Premium-Prediction\insurance.csv"
def Batch_predicter(database:bool,input_file_path=default_data_path):
    try:
        model_resolver = ModelResolver()
        os.makedirs(PREDICTION_DIR, exist_ok=True)
        if database is True:
            print('batch prediction going with 500 random dataset sample from mongodb!')
            logging.info(f"Creating model resolver object")
            logging.info(f"Reading file :{input_file_path}")
            df = utils.get_data(database=DATA_BASE_NAME,collection_name=COLLECTION_NAME)
            logging.info(f"loaded data from the mongodb for the batch prediction")
            df = df.sample(n=500) 


        else:
            print('batch prediction going with default dataset !')

            df = pd.read_csv(input_file_path)
           
        df.replace({"na": np.NAN}, inplace=True)
        # validation
        logging.info(f"Loading transformer to transform dataset")
        transformer_path = model_resolver.get_latest_transformer_path()
        transformer = utils.load_model(file_path=transformer_path)
        
       
        logging.info(f"Target encoder to convert predicted column into categorical")
        target_encoder = utils.load_model(file_path=model_resolver.get_latest_target_encoder_path())


        input_feature_names = os.getenv('INPUT_FEATURE_NAME').split(',')

        for i in input_feature_names:       
            if df[i].dtypes =='object':
                df[i] =target_encoder.fit_transform(df[i])
        logging.info(f"shape of the data before transformation")
        logging.info(f"{df[input_feature_names].shape} ")
        logging.info(f" input feature names :- {input_feature_names}")
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"Loading model to make prediction")
        model = utils.load_model(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        
        df["prediction"]=prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise InsuranceException(e, sys)