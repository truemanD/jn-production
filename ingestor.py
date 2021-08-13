from datetime import datetime

import nbformat
import logging
import requests
import configparser

tstart = datetime.now()
log_file = './logs/ingestor_' + tstart.__str__() + '.log'

logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

repo_url = config['ingestor']['repo_name']

nb_name = config['ingestor']['nb_name']

nb_url = repo_url + nb_name
r = requests.get(nb_url, allow_redirects=True)

with open('train/src/notebook/' + nb_name, 'w') as f:
    f.write(r.text)

ds_name = config['ingestor']['ds_name']

ds_url = repo_url + ds_name
r = requests.get(ds_url, allow_redirects=True)

with open('train/data/' + ds_name, 'w') as f:
    f.write(r.text)

log.info("All imported libs inserted in requerements.txt")
log.info("Train.py script prepared")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
