from datetime import datetime
import logging
import configparser
import os

tstart = datetime.now()
dir = 'logs/'
if not os.path.exists(dir):
    os.mkdir(dir)
log_file = 'logs/generator_' + tstart.__str__() + '.log'
logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

dir = 'predict'
if not os.path.exists(dir):
    os.mkdir(dir)
dir = 'predict/razum'
if not os.path.exists(dir):
    os.mkdir(dir)
dir = 'predict/docker'
if not os.path.exists(dir):
    os.mkdir(dir)
dir = 'train'
if not os.path.exists(dir):
    os.mkdir(dir)
dir = 'train/razum'
if not os.path.exists(dir):
    os.mkdir(dir)
dir = 'train/docker'
if not os.path.exists(dir):
    os.mkdir(dir)

# create DAGs for predict models
models = dict(config['models'].items())

for model_name in models:
    with open('utils/' + config['generator']['dag_predict_template'], 'r') as f:
        res = f.read()
        res = res.replace('<<model_name>>', model_name)
    with open('predict/razum/predict_' + model_name + '.py', 'w') as f:
        f.write(res)

    # create Dockerfile for predict
    with open('utils/' + config['generator']['docker_predict_template'], 'r') as f:
        res = f.read()
        res = res.replace('<<model_name>>', model_name)
    with open('predict/docker/Dockerfile.' + model_name, 'w') as f:
        f.write(res)


    # create DAG for train
    with open('utils/' + config['generator']['dag_train_template'], 'r') as f:
        res = f.read()
        res = res.replace('<<model_name>>', model_name)
    with open('train/razum/train_' + model_name + '.py', 'w+') as f:
        f.write(res)

    # create Dockerfile for train
    with open('utils/' + config['generator']['docker_predict_template'], 'r') as f:
        res = f.read()
        res = res.replace('<<model_name>>', model_name)
    with open('train/docker/Dockerfile.' + model_name, 'w') as f:
        f.write(res)


log.info("All things generated")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
