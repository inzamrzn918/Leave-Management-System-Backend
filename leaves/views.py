from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from leaves import services


@api_view(['GET'])
def my_leaves(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.get_leaves_by_token(token)
        return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid request parameter'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def manager_leaves(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.manager_leaves(token)
        return Response(response, status=status.HTTP_200_OK)
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid request parameter'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_leave(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        body = request.data
        response = services.request_leave(token, body)
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid request parameter',
            'code': status.HTTP_406_NOT_ACCEPTABLE

        }
    return Response(response, status=response['code'])

@api_view(['DELETE'])
def delete_leave(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        id = request.data.get("id")
        response = services.delete_leaves_requeste(token, id)
    except KeyError as e:
        response = {
            'status': False,
            'message': 'Invalid request parameter',
            'code': status.HTTP_406_NOT_ACCEPTABLE

        }
    return Response(response, status=response['code'])