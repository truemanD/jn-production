import pickle
from datetime import datetime

import nbformat
import logging

tstart = datetime.now()
log_file = 'logs/convertor_' + tstart.__str__() + '.log'

logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

# prepare requirement for predict
res = "pickle4\nflask\npandas"
with open('predict/src/scripts/requirements.txt', 'w') as f:
    f.write(res)


# convert to python for predict
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


def predict_api(model_name):
    res = "import pickle\n" \
          + "from flask import Flask, request, jsonify\n" \
          + "import traceback\n" \
          + "import pandas as pd\n" \
          + "app = Flask(__name__)\n" \
          + "@app.route('/predict', methods=['POST'])\n" \
          + "def predict():\n" \
          + "\tif model:\n" \
          + "\t\ttry:\n" \
          + "\t\t\tjson_ = request.json\n" \
          + "\t\t\tprint(json_)\n" \
          + "\t\t\tquery = pd.DataFrame(json_, index=[0])\n" \
          + "\t\t\tprediction = list(model.predict(query))\n" \
          + "\t\t\treturn jsonify({'prediction': str(prediction)})\n" \
          + "\t\texcept:\n" \
          + "\t\t\treturn jsonify({'trace': traceback.format_exc()})\n" \
          + "\telse:\n" \
          + "\t\tprint('Train the model first')\n" \
          + "\t\treturn ('No model here to use')\n" \
          + "if __name__ == '__main__':\n" \
          + "\tport = 12345\n" \
          + "\tmodel = pickle.load(open('predict/data/" + model_name + ".pkl', 'rb'))\n" \
          + "\tapp.run(port=port, debug=True)\n"

    with open('predict/src/api/' + model_name + '.py', 'w') as f:
        f.write(res)


# prepare requirements.txt for train
res = "pickle4\n"
with open('train/src/notebook/jupiter_notebook.ipynb') as f:
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

# convert to python for train
res = "import pickle\n"
with open('train/src/notebook/jupiter_notebook.ipynb') as f:
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
                        predict_api(model_name)
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

log.info("All imported libs inserted in requerements.txt")
log.info("Train.py script prepared")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())
