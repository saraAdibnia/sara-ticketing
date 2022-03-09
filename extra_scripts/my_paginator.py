from math import ceil
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination): # new custom pagination class for generic list views, use it in list api views
    page_size = 10
    page_size_query_param = 'items_per_page'
    page_query_param = 'page'
    max_page_size = 25

def my_paginator(query_list:iter, request): # old method of pagination in aseman avoid using thie approach as much as you can
    n = int(request.query_params.get('page', 1))
    items_per_page = int(request.query_params.get('items_per_page', 10))    
    return {'data': query_list.filter()[items_per_page*(n-1): items_per_page*(n)],
            'items_per_page': items_per_page,
            'pages': ceil(len(query_list)/ items_per_page)
            }
            
