import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import feature 
from sklearn import *
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl', 'rb'))

@app.route('/')
def predict1():
    return render_template('index.html')

@app.route('/predict')
def predict():
    return render_template('web.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        url = request.form['URL']
        checkprediction = feature.FeatureExtraction(url)
        prediction = model.predict(np.array(checkprediction.features).reshape(-1,30))
        print(prediction)
        output=prediction[0]
        if(output==1):
            pred="Your are safe!!  This is a Legitimate Website."
        else:
            pred="You are on the wrong site. Be cautious!"
        return render_template('web.html', prediction_text='{}'.format(pred),url=url)
    return render_template('web.html', prediction_text='{}'.format(pred),url=url)
@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

    

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)