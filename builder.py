from datetime import datetime
import logging

tstart = datetime.now()
log_file = 'logs/builder_' + tstart.__str__() + '.log'
logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

# build train module

# launch train module

# build and save predict module



log.info("All things built")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())


