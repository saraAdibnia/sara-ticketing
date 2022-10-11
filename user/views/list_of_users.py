from user.models import User
from math import ceil
from user.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from extra_scripts.EMS import existence_error

class UserListView(APIView):

    # permission_classes = [CorporateUsersPermission]

    def get(self, request):  # get all user_logs based on thier id and date period
        sort = request.query_params.get('sort' , '-id')
        allowed_filters = (
            "id",
            "history__date__gte",
            "history__date__lte",
            "history__log_kind",
            "fname__contains",
            "mobile__contains",
            "flname__contains",
            "role",
            "is_active",
            "confirmation",
        )
        kwargs = {}
        for key, value in request.query_params.items():
            if key in allowed_filters:
                kwargs.update({key: value})

        n = int(request.query_params.get("page", 1))
        items_per_page = int(request.query_params.get("items_per_page", 10))

        main_query = User.objects.filter(**kwargs).all()
        # if not main_query.exists():
        #     return existence_error("user")
        user_logs = main_query.order_by(sort)

        total_filtered = len(main_query)

        serialized_data = UserSerializer(user_logs, many=True).data

        response_json = {
            "total_filtered": total_filtered,
            "pages": ceil(total_filtered / items_per_page),
            "data": serialized_data,
        }

        return Response(response_json, status=200)