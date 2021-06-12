from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import json
import numpy as np
import pandas as pd

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Flask utils
from functools import wraps
from flask import Flask, redirect, url_for, request, render_template,abort,Response
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model20.h5'
excel = 'data.xlsx'
df = pd.read_excel(excel)
# Load your trained model
model = load_model(MODEL_PATH)
f_l = open('labels.json')
labels = json.load(f_l)
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
# print('Model loaded. Check http://127.0.0.1:5000/')

def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == 'qjhdsbvfihfajb':
            return view_function(*args, **kwargs)
        else:
            return Response(
        "400 BAD REQUEST",
        status=400,
    )
    return decorated_function

def model_predict(img_path, model):
    test_datagen = ImageDataGenerator(rescale=1. / 255)
    test_generator = test_datagen.flow_from_directory(
        img_path,
        target_size=(224, 224),
        batch_size=32,
        class_mode="categorical",
        shuffle=False)
    pred=model.predict_generator(test_generator,verbose=1)
    return pred

def model_data(weeds):
    data = dict()
    for weed in weeds:
        x = df[df['Botanical Name']==weed]
        if len(x):
            dic = {}
            dic['crop'] = []
            for row in x.itertuples(index=False, name='Pandas'):
                dic['name']=row[0]
                dic['common']=row[1]
                dic['category']=row[2]
                dic['telugu']=row[3]
                dic['crop'].append([row[4],row[5],row[6]])
            data[weed]=dic
        else:
            data[weed]={'name':weed}
    return data

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
@require_appkey
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads','test','test.jpg')
        folder_path = os.path.join(
            basepath, 'uploads')
        f.save(file_path)

        # Make prediction
        preds = model_predict(folder_path, model)
        # predicted_class_indices=np.argmax(preds,axis=1)
        best_2 = np.argsort(preds, axis=1)[:,-2:]
        # print(labels,predicted_class_indices)
        predictions = [[labels[str(k[1])],labels[str(k[0])]] for k in best_2]
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        result = str(predictions[0][0]),str(predictions[0][1])             # Convert to string
        data = model_data(result)
        return data
    return None


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()

