from insurance.pipeline.batch_prediction import Batch_predicter
from insurance.exception import InsuranceException
import os,sys
# from insurance.pipeline.training_pipeline import start_training_pipeline

file_path=r"C:\Users\Ranjit Singh\Desktop\insorance-Premium-Prediction\insurance.csv"
print(__name__)
if __name__=="__main__":
    try:
        #output_file = start_training_pipeline()
        prediction_file_path = Batch_predicter(database = True)
        print(prediction_file_path)
    except Exception as e:
        raise InsuranceException(e,sys)