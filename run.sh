#!/bin/bash

pip install -r 'requirements.txt' && python ingestor.py && python convertor.py && pip install -r 'train/src/scripts/requirements.txt' && python trainer.py && pip install -r 'predict/src/api/requirements.txt' && python predict/src/scripts/rfc_predict.py && python predict/src/api/rfc.py