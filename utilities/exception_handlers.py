from rest_framework.response import Response


def validation_error(serializer):
    return Response({
        'error':serializer.errors,
        'succeeded':False
    })

def existence_error(object:str):
    return Response({
        'error':f'object {object} does not exists',
        'succeeded':False
    })