from http.client import HTTPResponse
from urllib import response
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import services


# Create your views here.


@api_view(['POST'])
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        return Response(services.login(username, password))
    except KeyError as e:
        response = {'Key Error': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_account(request):
    try:
        response = services.create_account(request)
        return Response(response, status=status.HTTP_201_CREATED)
    except Exception as e:
        response = {'status': False, 'message': str(e)}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.logout(token)
        return Response(response, status=status.HTTP_202_ACCEPTED)
    except KeyError as e:
        print(e)
        response = {
            'status': False,
            'message': str(e)
        }
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def my_account(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.get_profile(token)
        return Response(response, status=status.HTTP_202_ACCEPTED)
    except KeyError as e:
        response = {
            'status': False,
            'message': str(e)
        }
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def session_info(request):
    # print(request.META['HTTP_AUTHORIZATION'])
    try:
        token = request.META['HTTP_AUTHORIZATION']
        response = services.get_session_info(token)
        return Response(response, status=status.HTTP_202_ACCEPTED)
    except KeyError as e:
        response = {
            'status': False,
            'message': str(e)
        }
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def validate_login(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        renew = request.data.get('renew')
        response = services.validate_login(token, renew)
        return Response(response, status=status.HTTP_202_ACCEPTED)
    except KeyError as e:
        response = {
            'status': False,
            'message': str(e)
        }
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def get_token_user(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        renew = request.data.get('renew')
        response = services.get_token_user(token)
        return Response(response, status=status.HTTP_202_ACCEPTED)
    except KeyError as e:
        response = {
            'status': False,
            'message': str(e)
        }
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
def onboard(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        # response = services.onboard()
    except KeyError as e:
        response = {
            'status': False,
            'message': str(e)
        }
        return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def get_user(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        user_info = request.GET.get("q")
        response = services.get_user(user_info, token)
    except KeyError:
        response = {
            'status': False,
            'code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Key Error'
        }
    return Response(response, status=response['code'])

@api_view(['POST'])
def password_validation(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        password = request.data.get("password")
        response = services.val_password(token, password)
    except KeyError as e:
        response = {
            'status':False,
            'message': str(e),
            'code':status.HTTP_400_BAD_REQUEST
        }
    return Response(response, status=response['code']) 

