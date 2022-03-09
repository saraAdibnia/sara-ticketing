from django.db import models
from django.db.models import JSONField
from extra_scripts.timestampmodel import TimeStampedModel

class Mymodel(TimeStampedModel):

    answer = JSONField(
        blank=True,
        null=True,
        help_text=''',
            contains jsons in a specific order in the list
            each json's key shows a warehouse id as an integer
            each json's value shows that the cargo has either reached there or not
            so the json values are booleans        
            '''
    )


from django.dispatch import receiver
from logging import Logger
from django.db.models.signals import post_save, pre_save
from icecream import ic
# @receiver(pre_save, sender = Mymodel)
# def handle_new_notif(sender, **kwargs):
#     new = kwargs.get('instance')
#     try:
#         old = sender.objects.get(id = new.id)
#         # my_model_fields = sender._meta.get_all_field_names()
#         # chagned_fields = filter(lambda field: getattr(old,field,None)!=getattr(new,field,None), my_model_fields)
#         for item in kwargs['update_fields']:
#             ic('this is vlaue of old :', getattr(old, item))
#             ic('this is vlaue of  :', getattr(new, item))

#         # logger.info(f'NOTIF CREATED : NOTIF : {notif}')
#     except:
#         pass
#     return None
# @receiver(post_save, sender = Currency)
# def handle_new_notif(sender, **kwargs):
#     ewb = kwargs.get('instance')
#     ic('this is 2 , ', ewb )
#     ic( 'in received data kwargs is :\n',kwargs)
#     # logger.info(f'NOTIF CREATED : NOTFI : {notif}')

#     return None

