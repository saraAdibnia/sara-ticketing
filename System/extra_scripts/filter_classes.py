from order.models import Waybill

from django_filters import rest_framework as filters


class WaybillFilters(filters.FilterSet):
    user__fname__contains = filters.CharFilter(field_name="user", lookup_expr='fname__contains')
    user__flname__contains = filters.CharFilter(field_name="user", lookup_expr='flname__contains')
    user__ename__contains = filters.CharFilter(field_name="user", lookup_expr='ename__contains')
    user__elname__contains = filters.CharFilter(field_name="user", lookup_expr='elname__contains')
    step = filters.NumberFilter(field_name= 'step', )
    import_pricing_step = filters.NumberFilter(field_name="import_pricing_step", )
    user__mobile__contains = filters.CharFilter(field_name='user', lookup_expr='mobile__contains') 

    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    # filter_kwargs = ('user__fname__contains', 'user__ename__contains',
    #                  'step', 'import_pricing_step', 'user__mobile__contains'
    #                  'user__flname__contains', 'user__elname__contains',)

    class Meta:
        model = Waybill
        fields = ['user', 'step']  

