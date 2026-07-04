import logging
import sys
import os 
from datetime import datetime


#Creates a unique log file name using the current date and time.
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


#Gets the current date and time.
#Formats it into a string.
#Creates the complete path where the log file will be stored.

##craetes apath where logs will be stored under logs folder
logs_path=os.path.join(os.getcwd(),"logs")

#"If the folder already exists, don't throw an error. Just continue."
os.makedirs(logs_path,exist_ok=True)
#it will join the current log and inside the logs path
LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)

##basic configuration of logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO

)
if __name__ == "__main__":
    logging.info("Logger is working!")
    logging.error("This is an error message.")

