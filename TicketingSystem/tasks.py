from celery import shared_task

@shared_task(name = 'add')
def add(x, y):
    z = x + y
    print(z)

