from contracts.serializers.import_contract_serialiser import ImportContractShowSerializer
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from contracts.models import ImportContract
from math import ceil
from rest_framework.response import Response


class UserContractView(APIView):
        
    permission_classes = [IsAuthenticated]

    def get(self, request):
        '''contract list'''

        allowed_filters = ('code__contains', 'start_date__lte', 'start_date__gte',
                           'expire_date__lte', 'expire_date__gte', 'canceled', 'finalized')
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.query_params.get('page', 1))
        items_per_page = int(request.query_params.get('items_per_page', 10))

        try:
            contract_objs = ImportContract.objects.filter(user=request.user.id, finalized=True).filter(
                **kwargs).order_by('-id')[items_per_page*(n-1): items_per_page*(n)]
        except IndexError:
            pass

        contract_serialized = ImportContractShowSerializer(
            contract_objs,
            many=True
        )

        total_filtered = ImportContract.objects.filter(
            user=request.user.id, finalized=True).filter(**kwargs).count()
        pages = ceil(total_filtered/items_per_page)

        response_json = {
            "succeded": True,
            "pages": pages,
            "total_filtered": total_filtered,
            "contract": contract_serialized.data
        }

        return Response(response_json, status=200)
