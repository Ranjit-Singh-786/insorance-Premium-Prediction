from insurance.pipeline.training_pipeline import RunTrainingPipeline
from insurance.logger import logging
from insurance.exception import InsuranceException
import os,sys
# to train the training Pipeline
if __name__ == "__main__":
    try:
        logging.info(f"Started Runing the Training Pipeline")
        RunTrainingPipeline()
    except Exception as e:
        raise InsuranceException(e,sys)
