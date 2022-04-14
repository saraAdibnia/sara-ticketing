from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from System.models import Ticket



@registry.register_document
class TicketDocument(Document):
    class Index:
        name = 'tickets'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Ticket
        fields = [
            'id',
            'title',
            'department',
            'user',
            'operator',
            'text',
            'tags',
            'is_answered',
            'kind',
            'status',
            'priority',
            'category',
        ]