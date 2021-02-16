import pickle
import pandas as pd
from flask import Flask, request, Response

from churn.Churn import churn # folder, file_name and class name

# Loading model
model = pickle.load(open('/home/edson/Projetos_DS/Client-Churn-Prediction/model/model_best_rf_selected.pkl', 'rb'))

# Initialize API
app = Flask(__name__)

@app.route('/churn/predict', methods=['POST'])
def churn_predict():
    test_json = request.get_json()

    if test_json: # There is data
        if isinstance(test_json, dict): # Unique example
            test_raw = pd.DataFrame(test_json, index=[0])

        else: # Multiple examples
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())


        # Instantiate churn class
        pipeline = churn()


        # Feature engineering
        df1 = pipeline.feature_engineering(test_raw)

        print(df1.shape)

        # Encoding
        df2 = pipeline.encoding(df1)


        # Prediction
        df_response = pipeline.get_prediction(model, test_raw, df2)

        return df_response

    else:
        return Response( '{}', status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

