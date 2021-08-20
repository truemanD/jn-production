#!/bin/bash

python ingestor.py && python convertor.py && python trainer.py && python predict/src/scripts/rfc_predict.py && python predict/src/api/rfc.py