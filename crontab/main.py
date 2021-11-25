import os
import signal

from croniter import croniter
from crontab import *
import json
import time
import logging


def get_jobs():
    try:
        crontab_path = config_data['CRONTAB_PATH']
        return CronTab(tabfile=crontab_path)
    except KeyError or NameError as e:
        logging.warning(e)
        exit(-1)


def cron():
    while True:
        my_cron = get_jobs()
        for string in my_cron:
            time_is_now = datetime.now()
            if croniter.match(str(string.slices), time_is_now):
                pid = os.fork()
                if pid == 0:
                    task = string.command
                    os.system(task)
                    logging.info(f"{time_is_now}: the task '{task}' is executed")
                    exit(0)
        time.sleep(60)


if __name__ == "__main__":
    main_path = os.path.split(__file__)[0]
    try:
        file = open(main_path + '/config.json', 'r')
        config_data = json.load(file)
        file.close()
    except NameError:
        exit(-1)
    try:
        log_level = config_data['LOG_LEVEL']
    except KeyError or NameError:
        exit(-1)
    try:
        log_path = config_data['LOG_PATH']
        logging.basicConfig(filename=log_path, level=log_level)
    except KeyError or NameError:
        exit(-1)

    logging.info("Start of program")
    cron()
