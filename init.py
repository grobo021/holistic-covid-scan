import os

import numpy as np
from flask import Flask, render_template, request, redirect, flash, send_from_directory
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    static_folder='./upload'
)

model = load_model('./model')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/images/<path:path>")
def send_image(path):
    return send_from_directory("templates/images", path)

@app.route("/", methods=["POST"])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join('upload', filename)
            file.save(path)

            img = image.load_img(path, target_size=(150, 150))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            images = np.vstack([x])
            classes = model.predict(images, batch_size=10)

            if classes == 0:
                label = 'COVID19'
            else:
                label = 'Normal'

            flash(label)
            flash(path)
            return redirect('/')


# start the flask app, allow remote connections
if __name__ == "__main__":
    app.secret_key = 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
    app.run(host='0.0.0.0')
