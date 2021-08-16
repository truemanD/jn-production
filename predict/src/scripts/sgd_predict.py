import pickle
sgd = pickle.load(open('predict/data/sgd.pkl','rb'))
X_test = pickle.load(open('predict/data/test_dataset.pkl','rb'))
y_test = pickle.load(open('predict/data/test_classes.pkl','rb'))
pred = sgd.predict(X_test)
result = sgd.score(X_test, y_test)
print('model score:', result)
