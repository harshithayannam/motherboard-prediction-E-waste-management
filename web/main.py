import os
from app import app
import urllib.request
from keras.preprocessing import image
from werkzeug.utils import secure_filename
import keras
import tensorflow as tf
global graph
graph = tf.compat.v1.get_default_graph()
import numpy as np
model =keras.models.load_model("predictions.h5")
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
from keras.applications.vgg16 import preprocess_input

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'files[]' not in request.files:
        flash('No file part')
        return redirect(request.url)
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        if file and allowed_file(file.filename):
            basepath = os.path.dirname(__file__)
            file_path = os.path.join(basepath, "static/uploads",secure_filename(file.filename)) #basepath 
            filename = secure_filename(file.filename)
            file.save(file_path)
            img = image.load_img(file_path,target_size = (64,64))
            x = image.img_to_array(img)
            x = np.expand_dims(x,axis = 0)
            x.shape
            pred = model.predict(x)
            print(pred)
            f=pred.astype(int)
            print(f)
            a1=np.array(f)
            print(a1)
            from functools import reduce
            single_list = reduce(lambda x,y: x+y, a1)
            print(single_list)
            val=np.where(single_list==1)
            dou_list = reduce(lambda x,y: x+y, val)
            print(dou_list)
            stringed = ''.join(map(str,val))
            stringed
            v=stringed[1]
            v1= int(v)
            v1
            index = ["IOports_Undamaged", "IOports_damaged", "Processor_Damaged", "Processor_Undamaged","atxconnector_Damaged","atxconnector_Undamaged","cmosbattery_Undamaged","cmosbattery_damaged"]
            cc={'url':file_path,'name':index[v1],'filename':filename}
            file_names.append(cc)
            print(file_names)
    return render_template('upload.html', filenames=file_names)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()




["Calf General wounds", "Calf Medical wounds", "Elbow General wounds", 
                     "Elbow Medical wounds", "Finger General wounds", "Finger Medical wounds", 
                     "Foot General wounds", "Foot Medical wounds", "Forehead General wounds", 
                     "Forehead Medical wounds", "Hand Nails General wounds", "Hand Nails Medical wounds", 
                     "Heel General wounds", "Heel Medical wounds", "Knee General wounds", 
                     "Knee Medical wounds", "Knuckles General wounds", "Knuckles Medical wounds",
                     "Palm General wounds", "Palm Medical wounds", "Shin General wounds", "Shin Medical wounds",
                     "Thighs General wounds", "Thighs Medical wounds", "Toes General wounds", "Toes Medical wounds"]