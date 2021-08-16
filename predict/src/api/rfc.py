import pickle
from flask import Flask, request, jsonify
import traceback
import pandas as pd
app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
	if model:
		try:
			json_ = request.json
			print(json_)
			query = pd.DataFrame(json_, index=[0])
			prediction = list(model.predict(query))
			return jsonify({'prediction': str(prediction)})
		except:
			return jsonify({'trace': traceback.format_exc()})
	else:
		print('Train the model first')
		return ('No model here to use')
if __name__ == '__main__':
	port = 12345
	model = pickle.load(open('predict/data/rfc.pkl', 'rb'))
	app.run(port=port, debug=True)
