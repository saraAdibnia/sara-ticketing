from django.utils import timezone


def get_date(**kwargs):
    '''Returns now, with the given parts overwritten'''
    dt = timezone.now()
    # optionally, depending on intended use of this function
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return dt.replace(**kwargs)
