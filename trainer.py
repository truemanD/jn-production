from datetime import datetime
import logging
import train.src.scripts.train as train

tstart = datetime.now()
log_file = 'logs/trainer_' + tstart.__str__() + '.log'

logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
log.info("All things trained")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
