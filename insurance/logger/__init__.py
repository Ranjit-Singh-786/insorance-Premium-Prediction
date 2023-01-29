# code for generate the logs
# logs will help to us, traverse the execution of our project.
import os
import logging
from datetime import datetime

LOG_DIRECTORY_NAME = "insurance_logs"
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
FILE_NAME =f"log_{CURRENT_TIME_STAMP}.log"
FILE_PATH = os.path.join(LOG_DIRECTORY_NAME,FILE_NAME)
os.makedirs(LOG_DIRECTORY_NAME,exist_ok=True)
logging.basicConfig(filename=FILE_PATH,
                    filemode="w",
                    level=logging.DEBUG,
                    format="[%(asctime)s]  - %(levelname)s - %(message)s")

# for the testing
if __name__ == "__main__": 
    logging.info(f"logging file testing !")