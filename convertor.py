import pickle
from datetime import datetime

import nbformat
import logging

tstart = datetime.now()
log_file = 'logs/convertor_' + tstart.__str__() + '.log'

logging.basicConfig(filename=log_file, filemode='w', format='%(levelname)s:%(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

# prepare requirements.txt
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
                    # print(words)
                    if len(words) > 0:
                        if words[0] == "import":
                            lib = words[1].split(".")
                            res = res + lib[0] + "\n"
                        if words[0] == "from":
                            lib = words[1].split(".")
                            res = res + lib[0] + "\n"

with open('train/src/scripts/requirements.txt', 'w') as f:
    f.write(res)

# convert to python
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
            elif cell.source.find('#dataset') > 0:
                rows = cell.source.split('\n')
                for row in rows:
                    # print(row)
                    arr = row.split('#')
                    # print(arr)
                    if arr[1] == 'dataset':
                        dataset_name = arr[0].split('\'')

                        print('dataset = ' + dataset_name[1])
                        row1 = dataset_name[0] + "\'train/data/" + dataset_name[1].split("/")[-1] + "\')"
                        # print(row1)
                        # res = res + cell.source + "\n"
                        res = res + row1 + "\n"
            else:
                res = res + cell.source + "\n"
with open('train/src/scripts/train.py', 'w') as f:
    f.write(res)

log.info("All imported libs inserted in requerements.txt")
log.info("Train.py script prepared")
tend = datetime.now()
log.info('Total execute time ' + (tend - tstart).__str__())

# filename = 'finalized_model.sav'
# pickle.dump(model, open(filename, 'wb'))