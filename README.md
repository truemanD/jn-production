пререквизиты )
```
pip install -r 'requirements.txt'
```
### 1. Загрузка JN и DS
на входе задаем в config.ini откуда брать JN и DS
```
[ingestor]
repo_name = https://raw.githubusercontent.com/...
ds_name = historical_dataset.csv
nb_name = jupiter_notebook.ipynb
```
запускаем модуль ingestor

```bash
python ingestor.py
```
DS и JN расположены в "правильных" местах репозитория

### 2. Конвертация JN в py скрипты
на входе имеем полученные ранее DS и JN

запускаем модуль convertor
```bash
python convertor.py
```

### 3. Обучение модели
на входе имеем сгенерированный файл train.py и данные для обучения модели в директории train/data

пререквизиты для обучения )
```
pip install -r 'train/src/scripts/requirements.txt'
```

запускаем модуль train

```
python train/src/scripts/train.py
```
