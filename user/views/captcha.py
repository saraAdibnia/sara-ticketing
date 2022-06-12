from rest_framework.response import Response
from rest_framework.views import APIView
import os
from utilities import validation_error, existence_error
from user.serializers import CaptchaSerializer
from user.models import Captcha
from extra_scripts.EMS import *

from captcha.image import ImageCaptcha
from extra_scripts.my_captcha import send_captcha
import uuid
from icecream import ic
class CaptchaView(APIView):
    """captcha views"""
    # TODO:
    def get(self, request):
        code = str(int(uuid.uuid4().int))[:5]
        filename = str(uuid.uuid4()).upper()[:7]
        path = './MEDIA/captcha/'+filename+'.png'
        ic(code)
        ic(path)
        # image.write(code, path)
        # captcha = send_captcha()
        image = ImageCaptcha(width=280, height=90)
        captcha = image.generate(code)
        image.write(code, captcha)
        captcha_serialized = CaptchaSerializer(
            data={'code': code, 'captcha': path[1:]})
        
        if not captcha_serialized.is_valid():
            return validation_error(captcha_serialized)
        captcha_serialized.save()
        

        response_json = {
            'succeeded': True,
            'captcha_info': {
                'id': captcha_serialized.data.get('id'),
                'captcha': captcha_serialized.data.get('captcha')
            }
        }

        return Response(response_json, status=200)

    def post(self, request):

        captcha_obj = Captcha.objects.filter(
            id=request.data.get('captcha_id')).first()
        if not captcha_obj:
            return existence_error('captcha')

        if request.data.get('code').upper() == captcha_obj.code:
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
