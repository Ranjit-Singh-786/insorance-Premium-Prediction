from insurance.logger import logging
from insurance.exception import InsuranceException
from insurance.utils import get_data
import os, sys

#code for testing the logger and exception file
# def log_except_tester():
#     try:
#         logging.info('enter in try blok of log_except_tester fun in main.py.')
#         test = 10/0
#         logging.info('executed try blok in log_except_tester fun in main.py.')
#     except Exception as e:
#         logging.info('error occured in log_except_tester fun in main.py')
#         obj = InsuranceException(e,sys)
#         logging.warning(obj.error_message)
#         logging.info('exception file successfully executed !')

# if __name__ == "__main__":
#     try:
#         logging.info('calling the function')
#         log_except_tester()
#     except Exception as e:
#         print(e)

# code for test the data loader
DATA_BASE_NAME = "insoranceDB"
COLLECTION_NAME  = "insoranceCL"
if __name__=="__main__":
    try:
        logging.info(f"start the data gathering process")
        get_data(DATA_BASE_NAME,COLLECTION_NAME )
    except Exception as e:
        logging.warning(f"data gathering operation failed")
        raise InsuranceException(e,sys)
