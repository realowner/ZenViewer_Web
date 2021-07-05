import logging
from datetime import date
from config import basedir

def main_logger():
    mlogger = logging.basicConfig(level=logging.INFO, filename=f'{basedir}/logs/app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # mlogger = logging.getLogger(f'main_app')
    # mlogger.setLevel(logging.INFO)
    # file_handler = logging.FileHandler(f'app.log', mode='w')
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # file_handler.setFormatter(formatter)
    # mlogger.addHandler(file_handler)

    return mlogger

def custom_logger(alg_name):
    today = date.today()
    curr_date = today.strftime('%d_%m_%Y')

    clogger = logging.getLogger(f'{alg_name}')
    clogger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(f'{basedir}/logs/viewer/{alg_name}_{curr_date}.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    clogger.addHandler(file_handler)

    return clogger