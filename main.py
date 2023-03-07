from insurance.pipeline.batch_prediction import Batch_predicter
from insurance.exception import InsuranceException
import os,sys

## to take the batch prediction

file_path=r"C:\Users\Ranjit Singh\Desktop\insorance-Premium-Prediction\insurance.csv"
print(__name__)
if __name__=="__main__":
    try:
        prediction_file_path = Batch_predicter(database = False)
        print(prediction_file_path)
    except Exception as e:
        raise InsuranceException(e,sys)