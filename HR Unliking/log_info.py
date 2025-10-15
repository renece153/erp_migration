#  ------------------ Importing Libraries ------------------------------
import logging
from datetime import date
import os

#  ------------------ Defining Logging Class ------------------------------
class system_log:

    def __init__(self, log_type):
        self.log_type = log_type
        self.log_directory = os.path.join(str(os.environ['SharedDrive']), 'DM','HR', 'Unlinking Logs', 'hr-dynamics-automation-' + date.today().strftime("%b-%d-%Y")+'.log')

    def chk_file_exists(self):
        file_exists = os.path.exists(self.log_directory)
        return 'a' if file_exists is True else 'w'

    def log_results(self, message):
        logging.basicConfig(filename=self.log_directory, filemode=self.chk_file_exists(), format='[%(levelname)s %(asctime)s] : %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %I:%M:%S %p')
        if self.log_type  == 'D':
            logging.debug(message)
        elif self.log_type  == 'I':
            logging.info(message)
        elif self.log_type == 'W':
            logging.warning(message)
        elif self.log_type  == 'E':
            logging.error(message)
        elif self.log_type  == 'C':
            logging.critical(message)

def error (_message:str):
    return system_log('E').log_results(_message)

def alert (_message:str):
    return system_log('I').log_results(_message)

def generate_header(_element:str, _message:str):
    mid = len(_message)//2 + 1
    fline = _element * (25 - mid)
    lline = _element * (25 - mid)
    return system_log('I').log_results(f"{fline}  {_message}  {lline}")
