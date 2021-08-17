import pickle
from datetime import datetime

import nbformat
import logging
import configparser

tstart = datetime.now()
log_file = 'logs/convertor_' + tstart.__str__() + '.log'
logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)
config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)


# prepare requirement for predict api
def reqs_predict_api():
    res = "pickle4\nflask\npandas"
    with open('predict/src/api/requirements.txt', 'w') as f:
        f.write(res)
    log.info("predict/src/api/requirements.txt prepared")


# prepare requirement for predict
def reqs_predict():
    res = "pickle4"
    with open('predict/src/scripts/requirements.txt', 'w') as f:
        f.write(res)
    log.info("predict/src/scripts/requirements.txt prepared")


# prepare requirements.txt for train
def reqs_train():
    res = "pickle4\n"
    with open('train/src/notebook/' + config['convertor']['jn_name']) as f:
        nb = nbformat.read(f, as_version=4)
        if not nb:
            pass
        for cell in nb.cells:
            if (cell.cell_type == 'code'):
                if cell.source.find("import") > 0:
                    strings = cell.source.split('\n');
                    for str in strings:
                        words = str.split();
                        if len(words) > 0:
                            if words[0] == "import":
                                lib = words[1].split(".")
                                res = res + lib[0] + "\n"
                            if words[0] == "from":
                                lib = words[1].split(".")
                                res = res + lib[0] + "\n"

    with open('train/src/scripts/requirements.txt', 'w') as f:
        f.write(res)

    log.info('train/src/scripts/requirements.txt prepared')


# convert JN to python for predict
def predict(model_name):
    res = "import pickle\n"
    res = res + model_name + " = pickle.load(open('predict/data/" + model_name + ".pkl','rb'))\n" \
          + "X_test = pickle.load(open('predict/data/test_dataset.pkl','rb'))\n" \
          + "y_test = pickle.load(open('predict/data/test_classes.pkl','rb'))\n" \
          + "pred = " + model_name + ".predict(X_test)\n" \
          + "result = " + model_name + ".score(X_test, y_test)\n" \
          + "print('model score:', result)\n"

    with open('predict/src/scripts/' + model_name + '_predict.py', 'w') as f:
        f.write(res)

    log.info('predict/src/scripts/' + model_name + '_predict.py prepared')


# convert JN to python for predict_api
def predict_api(model_name, port):
    with open('utils/' + config['convertor']['api_template'], 'r') as f:
        res = f.read()
        res = res.replace('<<model_name>>', model_name)
        res = res.replace('<<port>>', str(port))
    with open('predict/src/api/' + model_name + '.py', 'w') as f:
        f.write(res)

    log.info('predict/src/api/' + model_name + '.py prepared')


# convert JN to python for train
def train():
    port = int(config['convertor']['start_port'])
    res = "import pickle\n"
    with open('train/src/notebook/' + config['convertor']['jn_name']) as f:
        nb = nbformat.read(f, as_version=4)
    if not nb:
        pass
    for cell in nb.cells:
        row1 = ""
        row2 = ""
        if (cell.cell_type == 'code'):
            if cell.source.find('#model=') > 0:
                rows = cell.source.split('\n')
                for row in rows:
                    arr = row.split('=')
                    if arr[0] == '#model':
                        model_name = arr[1]
                        print('model_name = ' + model_name)
                        row1 = "filename = 'predict/data/" + model_name + ".pkl'\n"
                        row2 = "pickle.dump(" + model_name + ", open(filename, 'wb'))\n"
                        res = res + cell.source + "\n"
                        res = res + row1 + "\n"
                        res = res + row2 + "\n"
                        predict(model_name)
                        predict_api(model_name, port)
                        port = int(port) + 1
                        config_generator(model_name)
            elif cell.source.find('#test_dataset=') > 0 and cell.source.find('#test_classes=') > 0 and cell.source.find(
                    '#train_dataset=') > 0 and cell.source.find('#train_classes=') > 0:
                rows = cell.source.split('\n')
                for row in rows:
                    arr = row.split('=')
                    if arr[0] == '#test_dataset':
                        test_dataset = arr[1]
                        print('test_dataset = ' + test_dataset)
                        row1 = "pickle.dump(" + test_dataset + ", open('predict/data/test_dataset.pkl', 'wb'))"
                    elif arr[0] == '#test_classes':
                        test_classes = arr[1]
                        print('test_classes = ' + test_classes)
                        row3 = "pickle.dump(" + test_classes + ", open('predict/data/test_classes.pkl', 'wb'))"
                    elif arr[0] == '#train_classes':
                        train_classes = arr[1]
                        print('train_classes = ' + train_classes)
                        row5 = "pickle.dump(" + train_classes + ", open('train/data/train_classes.pkl', 'wb'))"
                    elif arr[0] == '#train_dataset':
                        train_dataset = arr[1]
                        print('train_dataset = ' + train_dataset)
                        row7 = "pickle.dump(" + train_dataset + ", open('train/data/train_dataset.pkl', 'wb'))"
                res = res + cell.source + "\n"
                res = res + row1 + "\n"
                res = res + row3 + "\n"
                res = res + row5 + "\n"
                res = res + row7 + "\n"
            elif cell.source.find('#dataset') > 0:
                rows = cell.source.split('\n')
                for row in rows:
                    arr = row.split('#')
                    if arr[1] == 'dataset':
                        dataset_name = arr[0].split('\'')
                        print('dataset = ' + dataset_name[1])
                        row1 = dataset_name[0] + "\'train/data/" + dataset_name[1].split("/")[-1] + "\')"
                        res = res + row1 + "\n"
            else:
                res = res + cell.source + "\n"
    with open('train/src/scripts/train.py', 'w') as f:
        f.write(res)

    log.info('train/src/scripts/train.py prepared')


def config_generator(model_name):
    config.set('models', model_name, model_name)
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def main():
    reqs_predict()
    reqs_predict_api()
    reqs_train()
    train()

    log.info("Script converted to artifacts")
    tend = datetime.now()
    log.info('Total execute time ' + (tend - tstart).__str__())


if __name__ == "__main__":
    main()
