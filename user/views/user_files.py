import re
from user.models import UserFiles
from rest_framework.views import APIView
from user.serializers.user_serializers import UserFilesSerialzier
from rest_framework.response import Response
from utilities import validation_error, existence_error 
from rest_framework.permissions import IsAuthenticated


class UserFileManager(APIView):  # TODO set permissions

    permission_classes = [IsAuthenticated]
    # get the reuqest user files

    def get(self, request):
        # TODO only user can see thier own files not other users.
        files = UserFiles.objects.filter(
            user=request.user.id, deleted=False)
        jr = UserFilesSerialzier(files, many=True)
        return Response({'data': jr.data}, status=200)

    def post(self, request):
        # create one user file for request user
        data = {
            'file': request.data.get('file'),
            'user': request.user.id,
            'name': request.data.get('name'),
        }
        serializer = UserFilesSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return validation_error(serializer)
        return Response({'succeeded': True}, status=200)

    def delete(self, request):
        # soft delete on UserFile for request.user
        file = UserFiles.objects.filter(
            id=request.query_params.get('id')).first()
        if not file:
            return existence_error('file object')
        if file.user != request.user:
            return Response({'description': 'این فایل متعلق به شما نیست و  شما نمی توانید ان را حذف کنید '}, status=403)

        serializer = UserFilesSerialzier(
            instance=file,  data={'deleted': True})
        if serializer.is_valid():
            serializer.save()
        else:
            return validation_error(serializer)
        return Response({'succeeded': True}, status=200)
