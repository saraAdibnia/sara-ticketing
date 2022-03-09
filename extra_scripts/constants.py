import math
from price.models.constant_models import Constant
from extra_scripts import roundNumber
from price.serializers import ConstantSerializer
from icecream import ic

def LastConstByCodeAndDate(code=1, date=None):
    if date is None:
        constant_obj = Constant.objects.filter(code=code).first()
    else:
        ic(date)
        constant_obj = Constant.objects.filter(
            code=code, start_date__lte=date, end_date__gt=date
        ).last()
    
    return constant_obj.value

