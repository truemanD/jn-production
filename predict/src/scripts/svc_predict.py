import pickle
svc = pickle.load(open('predict/data/svc.pkl','rb'))
X_test = pickle.load(open('predict/data/test_dataset.pkl','rb'))
y_test = pickle.load(open('predict/data/test_classes.pkl','rb'))
pred = svc.predict(X_test)
result = svc.score(X_test, y_test)
print('model score:', result)
