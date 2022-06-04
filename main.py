import os
import PIL
from flask import Flask, request, jsonify
from PIL import Image
import base64
import numpy as np
import cv2
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_image():
    
    f = request.files['image'].read()
    # print('-------------',f)
    # f.save(secure_filename(f.filename))

    npimg = np.frombuffer(f,np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    _, buff = cv2.imencode('.png',grayscale)
    b64 = base64.b64encode(buff).decode("utf-8")
    
    

    

    return jsonify({
        'success': b64,
        'file': 'Received'
    })



if __name__ == "__main__":
    app.run(debug=True)