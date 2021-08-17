from datetime import datetime
import logging
import configparser

tstart = datetime.now()
log_file = 'logs/generator_' + tstart.__str__() + '.log'
logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

models = dict(config['models'].items())
# print(type(models))
# print(models)

res = ''
for model_name in models:
    with open('utils/DAG.template', 'r') as f:
        res = f.read()
        # print(res)
        res = res.replace('<<model_name>>', model_name)
        # print(res)
    with open('predict/razum/' + model_name + '.py', 'w') as f:
        f.write(res)


log.info("All thing genarated")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
