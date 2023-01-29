from insurance.logger import logging
from insurance.exception import InsuranceException
import os, sys
def log_except_tester():
    try:
        logging.info('enter in try blok of log_except_tester fun in main.py.')
        test = 10/0
        logging.info('executed try blok in log_except_tester fun in main.py.')
    except Exception as e:
        logging.info('error occured in log_except_tester fun in main.py')
        obj = InsuranceException(e,sys)
        logging.warning(obj.error_message)
        logging.info('exception file successfully executed !')

if __name__ == "__main__":
    try:
        logging.info('calling the function')
        log_except_tester()
    except Exception as e:
        print(e)
