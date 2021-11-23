from croniter import croniter
from crontab import *
import json
import time
import logging

# connecting to files
dir_name = os.path.split(__file__)
try:
    f = open(dir_name[0] + '/config.json', 'r')
    config_data = json.load(f)
    f.close()
except NameError:
    raise SystemExit

try:
    log_level = config_data['LOG_LEVEL']
except KeyError or NameError as e:
    raise SystemExit

try:
    log_path = config_data['LOG_PATH']
    logging.basicConfig(filename=log_path, level=log_level)
    logging.info("Initialization of logs")
except KeyError or NameError as e:
    logging.warning(e)
    raise SystemExit

try:
    crontab_path = config_data['CRONTAB_PATH']
    my_cron = CronTab(tabfile=crontab_path)
    logging.info("Start crontab...")
except KeyError or NameError as e:
    logging.warning(e)
    raise SystemExit

# processing and accomplish commands
while True:
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
