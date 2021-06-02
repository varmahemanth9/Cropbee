from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'models/model.h5'

# Load your trained model
model = load_model(MODEL_PATH)
labels = {0: 'Achyranthes aspera',
 1: 'Amaranthus viridis',
 2: 'Argemone mexicana',
 3: 'Chenopodium album',
 4: 'Chloris barbata',
 5: 'Cleome viscosa',
 6: 'Cynodon dactylon',
 7: 'Cyperus rotundus',
 8: 'Dactyloctenium aegyptium',
 9: 'Digitaria sanguinalis',
 10: 'Leersia hexandra',
 11: 'Melilotus indicus',
 12: 'Ocimum americanum',
 13: 'Oxalis corniculata',
 14: 'Oxalis latifolia',
 15: 'Portulaca oleracea',
 16: 'Striga asiatica',
 17: 'Tridax procumbens',
 18: 'Triumfetta rhomboidea'}
# model._make_predict_function()          # Necessary
# print('Model loaded. Start serving...')

# You can also use pretrained model from Keras
# Check https://keras.io/applications/
#from keras.applications.resnet50 import ResNet50
#model = ResNet50(weights='imagenet')
#model.save('')
# print('Model loaded. Check http://127.0.0.1:5000/')


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


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
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
        predicted_class_indices=np.argmax(preds,axis=1)
        predictions = [labels[k] for k in predicted_class_indices]
        # Process your result for human
        # pred_class = preds.argmax(axis=-1)            # Simple argmax
        result = str(predictions[0])             # Convert to string
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)

