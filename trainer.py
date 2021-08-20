from datetime import datetime
import logging
import train.src.scripts.train as train
import os

tstart = datetime.now()

dir = 'logs/'
if not os.path.exists(dir):
    os.mkdir(dir)

log_file = 'logs/trainer_' + tstart.__str__() + '.log'

logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
log.info("All things trained")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
