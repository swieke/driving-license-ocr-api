from flask import Flask, render_template, flash, redirect, request, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from FullBuild import SimExtract
import hashlib
import os
import json

app = Flask(__name__)


@app.route("/")
def index():
        return render_template('index.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
        if 'mySIM' in request.files:
                image = request.files['mySIM']
                filename = image.filename
                filename = filename.strip('.')[0]
                filename = hashlib.md5(filename.encode())
                filename = filename.hexdigest()
                filename = "sim_{}_card.jpg".format(filename)
                filename = secure_filename(filename)
                path = os.path.join('./src/', filename)
                image.save(path)

                
                output, filename = SimExtract(image, filename)
                output = jsonify(**output)
        return output

@app.route('/src/<path:filename>')
def image(filename):
        return send_from_directory('./src/',filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
