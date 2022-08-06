from celery import shared_task
from System.models import Ticket
@shared_task(name='to_suspend')
def to_suspend():
    tickets = Ticket.objects.filter(status = 0).all()
    tickets.status = 3
    tickets.save()
    return tickets
