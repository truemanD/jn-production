import pickle
rfc = pickle.load(open('predict/data/rfc.pkl','rb'))
X_test = pickle.load(open('predict/data/test_dataset.pkl','rb'))
y_test = pickle.load(open('predict/data/test_classes.pkl','rb'))
pred = rfc.predict(X_test)
result = rfc.score(X_test, y_test)
print('model score:', result)
