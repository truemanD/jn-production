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
jn_name = jupiter_notebook.ipynb
```
запускаем модуль ingestor

```bash
python ingestor.py
```
DS и JN расположены в "правильных" местах репозитория

#### HoTo
В среде Jupiter Notebook в файле ipynb необходимо сделать ряд пометок:

1. тегом #dataset помечаем строку в ячейке, где осуществляется импорт датасета
```
wine = pd.read_csv('./../../data/historical_dataset.csv') #dataset
```
2. тегами
```
#test_dataset=X_test
#test_classes=y_test
#train_dataset=X_train
#train_classes=y_train
```
создаются указатели на переменные с наборами данных для обучения модели и ее тестирования

3. тегами 

```
#model=sgd
```
создаются указатели на переменные с обученными моделями

!все указатели должны находиться в тех ячейках, где происходит инициализациия необходимых переменных

### 2. Конвертация JN в py скрипты
на входе имеем полученные ранее DS и JN. Pадаем в config.ini откуда брать JN и DS
```
[convertor]
jn_name = jupiter_notebook.ipynb
```

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

### 4. Использование модели
пререквизиты для использования )
```
pip install -r 'predict/src/scripts/requirements.txt'
```

запускаем модуль predict

```
python predict/src/scripts/predict.py
```

### 5. Генерация сценария расчета(DAG) и политик доступа(REGO)
запускаем модуль генерации DAG
```
python generator.py
```

### 6. Сборка модуля обучения и модуля использования модели





