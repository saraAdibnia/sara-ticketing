from rest_framework.response import Response
from rest_framework.views import APIView
from captcha.image import ImageCaptcha
from rest_framework import status
import uuid
import os
from utilities import validation_error, existence_error
from user.serializers import CaptchaSerializer
from user.models import Captcha
from extra_scripts.EMS import *
from django.http import HttpResponseRedirect

import cv2
import string
import glob2
import random
from PIL import ImageFont, ImageDraw, Image
import numpy as np
class CaptchaView(APIView):
    # Setting up the canvas
    size = random.randint(10,16)
    length = random.randint(4,8)
    img = np.zeros(((size*2)+5, length*size, 3), np.uint8)
    img_pil = Image.fromarray(img+255)

    # Drawing text and lines
    font_path = r'C:\Windows\Fonts'
    fonts=glob2.glob(font_path+'\\ari*.ttf')
    font = ImageFont.truetype(random.choice(fonts), size)
    draw = ImageDraw.Draw(img_pil)
    text = ''.join(
    random.choice(string.ascii_uppercase+ string.digits + string.ascii_lowercase) 
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

    #Displaying image
    cv2.imshow(f"{text}", img)
    cv2.waitKey()
    cv2.destroyAllWindows()





# class CaptchaView(APIView):
    #TODO:
    # def get(self, request):
    #     code = str(uuid.uuid4().int)[:5]
    #     filename = str(uuid.uuid4()).upper()[:7]
    #     image = ImageCaptcha()
    #     path = './MEDIA/captcha/'+filename+'.png'
    #     print(code)
    #     print(filename)
    #     image.write(code, path)


    #     captcha_serialized = CaptchaSerializer(data={'code': code, 'captcha': path[1:]})
    #     if not captcha_serialized.is_valid():
    #         return validation_error(captcha_serialized)
    #     captcha_serialized.save()

    #     response_json = {
    #         'succeeded': True,
    #         'captcha_info': {
    #             'id': captcha_serialized.data.get('id'),
    #             'captcha': captcha_serialized.data.get('captcha')
    #         }
    #     }

    #     return Response(response_json, status=200)

    def post(self, request):


        captcha_obj = Captcha.objects.filter(id=request.data.get('captcha_id')).first()
        if not captcha_obj:
            return existence_error('captcha')
        
        if request.data.get('code').upper()==captcha_obj.code:
            response_json = {
                'succeeded': True
            }
        else:
            response_json = {
                'succeeded': False
            }

        os.remove('.'+captcha_obj.captcha)
        captcha_obj.delete()

        return Response(response_json, status=200)
