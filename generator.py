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

# create DAGs for predict models
models = dict(config['models'].items())
res = ''
for model_name in models:
    with open('utils/' + config['generator']['dag_predict_template'], 'r') as f:
        res = f.read()
        res = res.replace('<<model_name>>', model_name)
    with open('predict/razum/' + model_name + '.py', 'w') as f:
        f.write(res)

# create DAG for train
res = ''
project_name = config['common']['project_name']
with open('utils/' + config['generator']['dag_train_template'], 'r') as f:
    res = f.read()
    res = res.replace('<<project_name>>', project_name)
with open('train/razum/train_' + project_name + '.py', 'w') as f:
    f.write(res)

# create Dockerfile for train
res = ''
project_name = config['common']['project_name']
with open('utils/' + config['generator']['docker_train_template'], 'r') as f:
    res = f.read()
    res = res.replace('<<project_name>>', project_name)
with open('train/docker/Dockerfile', 'w') as f:
    f.write(res)

# create Dockerfile for predict
res = ''
project_name = config['common']['project_name']
with open('utils/' + config['generator']['docker_predict_template'], 'r') as f:
    res = f.read()
    res = res.replace('<<project_name>>', project_name)
with open('predict/docker/Dockerfile', 'w') as f:
    f.write(res)


log.info("All things generated")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
