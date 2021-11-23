from croniter import croniter
from crontab import *
import json
import time
import logging


# connecting to files
dir_name = os.path.split(__file__)
try:
    with open(dir_name[0] + '/config.json', 'r') as f:
        data = json.load(f)
except NameError:
    raise SystemExit

try:
    log_level = data['LOG_LEVEL']
except KeyError or NameError as e:
    raise SystemExit

try:
    log_path = data['LOG_PATH']
    logging.basicConfig(filename=log_path, level=log_level)
    logging.info("Initialization of logs")
except KeyError or NameError as e:
    logging.warning(e)
    raise SystemExit

try:
    crontab_path = data['CRONTAB_PATH']
    my_cron = CronTab(tabfile=crontab_path)
    logging.info("Start crontab...")
except KeyError or NameError as e:
    logging.warning(e)
    raise SystemExit

line_crontab = my_cron.commands
set_lines = dict()


def parse():
    try:
        index = 0
        while True:
            item_value = line_crontab.__next__()
            line = my_cron.__getitem__(index)
            item_key = str(line)[:str(line).find(item_value)]
            index += 1
            if item_key in set_lines:
                set_lines[item_key] += [item_value]
            else:
                set_lines[item_key] = [item_value]
    except StopIteration:
        logging.info("Time and command recording")


# processing and accomplish commands
while True:
    parse()
    for key in set_lines:
        time_is_now = datetime.now()
        for item in set_lines[key]:
            if croniter.match(key, time_is_now):
                pid = os.fork()
                if pid == 0:
                    os.system(item)
                    logging.info(f"{time_is_now}: the task '{item}' is executed")
                    exit(0)
    time.sleep(60)
