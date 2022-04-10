import cv2
import string
import glob2
import uuid
import random
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from rest_framework.response import Response
from user.serializers import CaptchaSerializer
from utilities import validation_error
def send_captcha():
    # Setting up the canvas
    size = random.randint(15,22)
    length = random.randint(5,6)
    img = np.zeros(((size*2)+5, length*size, 3), np.uint8)
    img_pil = Image.fromarray(img+255)
    # Drawing text and lines
    font_path = r'C:\Windows\Fonts'
    fonts=glob2.glob(font_path+'\\ari*.ttf')
    font = ImageFont.truetype(random.choice(fonts), size)
    draw = ImageDraw.Draw(img_pil)
    text = ''.join(
    random.choice(string.digits) 
               for _ in range(length))
    draw.text((5, 10), text, font=font, 
    fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    draw.line([(random.choice(range(length*size)), random.choice(range((size*2)+5)))
        ,(random.choice(range(length*size)), random.choice(range((size*2)+5)))]
        , width=1, fill=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

    # Adding noise and blur
    img = np.array(img_pil)
    thresh = random.randint(1,5)/100
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            rdn = random.random()
            if rdn < thresh:
                img[i][j] = random.randint(0,123)
            elif rdn > 1-thresh:
                img[i][j] = random.randint(123,255)
    img = cv2.blur(img,(int(size/random.randint(5,10)),int(size/random.randint(5,10))))
    code = str(uuid.uuid4().int)[:5]
    #Displaying image
    path = './MEDIA/captcha/'+code+'.png'
    cv2.imwrite(path, img)
    return {
        'code' : text ,
        'path': path
    }
    