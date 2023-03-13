from flask import Flask, render_template
from flask import request
import sqlite3
from werkzeug.utils import secure_filename

import numpy as np
from PIL import Image
import tensorflow as tf
import cv2
from tensorflow import keras

import model
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

mod = keras.models.load_model('waste_mobile_without.h5')

@app.route('/home')
@app.route('/')
def HomePage():  # put application's code here
    return model.HomePage()


@app.route('/InfoHome')
@app.route('/InfoHome/<int:section_id>', methods=['GET'])
def InfoPage(section_id=0):
    # section_id = request.values.get("section_id")
    if section_id == 0:
        path = "impact.html"
    elif section_id == 1:
        path = "reuse.html"
    elif section_id == 2:
        path = "analysis.html"
    else:
        path = None

        # if path:
    last_dot_index = path.rfind(".")
    title = path[:last_dot_index]
    with open("templates/InfoPages/%s" % path, "r") as f:
        content = f.read()

    return model.InfoPage(section_id, title=title, content=content)

# AI model prediction
def predict_cls(img):
    classes = ['ORGANIC', 'RECYCLABLE']
    SIZE = 128

    final_img = np.expand_dims(cv2.resize(img, (SIZE, SIZE)), axis=0)
    probs = mod(final_img)
    return classes[np.argmax(probs)]

@app.route('/sorting', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']

        img = Image.open(f)
        np_img = np.array(img)

        cls = predict_cls(np_img)
        
        print(request.files)
        f.save(secure_filename(f.filename))

        return model.resultPage(cls)
    else:
        return model.sortingPage()

@app.route('/about')
def aboutpage():
    return model.AboutPage()


@app.route('/map')
def mappage():
    return model.MapPage()

if __name__ == '__main__':
    app.run(debug=True)
