import os
import PIL
from flask import Flask, request, jsonify
from PIL import Image
import base64
import numpy as np
import cv2
from sqlalchemy import null
from werkzeug.utils import secure_filename
from skimage import color, img_as_float


app = Flask(__name__)

def hsv(img, l, u):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([l,128,128]) # setting lower HSV value
    upper = np.array([u,255,255]) # setting upper HSV value
    mask = cv2.inRange(hsv, lower, upper) # generating mask
    return mask

def exponential_function(channel, exp):
    table = np.array([min((i**exp), 255) for i in np.arange(0, 256)]).astype("uint8") # creating table for exponent
    channel = cv2.LUT(channel, table)
    return channel


def tone(img, number):
    for i in range(3):
        if i == number:
            img[:, :, i] = exponential_function(img[:, :, i], 1.05) # applying exponential function on slice
        else:
            img[:, :, i] = 0 # setting values of all other slices to 0
    return img


def sepia(img):
    img = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])) 
    img[np.where(img > 255)] = 255 
    img = np.array(img, dtype=np.uint8)

    return img


def splash(img):

    res = np.zeros(img.shape, np.uint8) # creating blank mask for result
    l = 15 # the lower range of Hue we want
    u = 30 # the upper range of Hue we want
    mask = hsv(img, l, u)
    inv_mask = cv2.bitwise_not(mask) # inverting mask
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res1 = cv2.bitwise_and(img, img, mask= mask) # region which has to be in color
    res2 = cv2.bitwise_and(gray, gray, mask= inv_mask) # region which has to be in grayscale
    for i in range(3):
        res[:, :, i] = res2 # storing grayscale mask to all three slices
    img = cv2.bitwise_or(res1, res) # joining grayscale and color region
    return img

def sharpen(img,val,sh):
    img_c = img.copy()
    if (val == 1):
        kernel = np.array([[-1, -1, -1], [-1, sh, -1], [-1, -1, -1]])
        img_sharpen = cv2.filter2D(img, -1, kernel)
        return img_sharpen
    elif (val == 0):
        return img_c 

    
def duo_tone(img):
    img = tone(img, 0)

    return img

def exposure(img):
#read image
    

    #edge detection filter
    kernel = np.array([[0.1, -1.0, 0.0], 
                    [-1.0, 4.0, -1.0],
                    [0.0, -1.0, 0.0]])

    kernel = kernel/(np.sum(kernel) if np.sum(kernel)!=0 else 1)

    #filter the source image
    img_rst = cv2.filter2D(img,-1,kernel)

    #save result image
    return img

def blur(img):
    ksize = (10, 10)
    
    # Using cv2.blur() method 
    image = cv2.blur(img, ksize) 
    return image




def cartoon(img):

# Edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                         cv2.THRESH_BINARY, 9, 9)
   
# Cartoonization
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
   
    return cartoon


def im(img):

    sha = sharpen(img,1)
    cartn = cartoon(sha)
    blur_ = blur(cartn)
    
    m1 = [0.6, 0.8, 0.7]

    co = m1 *blur_
    
    co = co*[0.6]
    
    return co

@app.route("/", methods=["POST"])
def process_image():
    
    f = request.files['image'].read()
    # print('-------------',f)
    # f.save(secure_filename(f.filename))

    npimg = np.frombuffer(f,np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img_r = cv2.resize(img, (450,450))

    _, biff = cv2.imencode('.png',img_r)
    origb64 = base64.b64encode(biff).decode("utf-8")


    
    # ex = exposure(img_r)
    # sha = sharpen(img_r,1)
    cartn = cartoon(img_r)
    # blur_ = blur(cartn)

    grayscale = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
    ss =splash(img_r)
    s = duo_tone(img_r)

    
    # co = color.gray2rgb(grayscale)
    # m1 = [0.6, 0.8, 0.7]
    # co_ = (img_r*[0.2])

    # print(co_)

    _, buff = cv2.imencode('.png',s)
    b64 = base64.b64encode(buff).decode("utf-8")
    
    return jsonify({
        'original': b64,
        'new': origb64,
        'file': 'Received'
    })



@app.route("/game", methods=["POST"])
def game():
    f = request.files['image'].read()
    
    npimg = np.frombuffer(f,np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img_r = cv2.resize(img, (450,450))

    conditions = request.form
    print(conditions)
    img_ = img_r   

    # if (conditions['sharpen'] != null):
    #     img_ = sharpen(img_,1,float(conditions['sharpen']))
    # if (conditions['brightness'] != null):
    #     img_ = img_ * float(conditions['brightness'])
    if (conditions['splash'] != null):
        img_ = splash(img_)
    if (conditions['duo_tone'] != null):
        img_ = duo_tone(img_)    
    
        


    _, biff = cv2.imencode('.png',img_)
    b64 = base64.b64encode(biff).decode("utf-8")

    return jsonify({
        'img': b64,
        'file': 'Received'
    })
    


if __name__ == "__main__":
    app.run(debug=True)