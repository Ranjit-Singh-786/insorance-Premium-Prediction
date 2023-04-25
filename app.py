from flask import Flask, render_template, request, url_for, redirect
import joblib
from sklearn.preprocessing import LabelEncoder
# from insurance import utils
import pandas as pd
import numpy as np
import sklearn
import gunicorn
import xgboost
import pickle

model_path = r"C:\Users\Ranjit Singh\Desktop\insorance-Premium-Prediction\saved_models\4\model\trained_model.pkl"
label_encoder_path = r"C:\Users\Ranjit Singh\Desktop\insorance-Premium-Prediction\saved_models\4\target_encoder\label_encoder.pkl"
transformer_path = r"C:\Users\Ranjit Singh\Desktop\insorance-Premium-Prediction\saved_models\4\target_encoder\label_encoder.pkl"

# load our model file
model = pickle.load(open(model_path,'rb'))
label_encoder = pickle.load(open(label_encoder_path,'rb'))
transformer = pickle.load(open(transformer_path,'rb'))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
 
        age = int(request.form['age'])
        sex = str(request.form['sex'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])     # children range 0 - 5
        smoker = str(request.form['smoker'])
        region = str(request.form['region'])

        # 2. create DataFrame
        data = [[age, sex, bmi, children, smoker,region]]
        column_name = ['age', 'sex', 'bmi', 'children', 'smoker','region']
        
        data_model = pd.DataFrame(data, columns=column_name)
        # return str(data_model.loc[0])




# Transformation the data

        ### label encoding
        for col in data_model.columns:
            if data_model[col].dtypes == 'O':
                data_model[col] = label_encoder.fit_transform(data_model[col])
            else:
                # else do nothing
                data_model[col] = data_model[col]

        ### imputer &&& RobustScaler

        # transformed_data = transformer.transform(data_model[column_name].values[0])
 

        # Prediction
        result = model.predict(data_model)[0]

        result= round(float(result), 2)

        # 3. Display

        return render_template('index.html', Predict_Text=f'Predict Premium is {result}')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
