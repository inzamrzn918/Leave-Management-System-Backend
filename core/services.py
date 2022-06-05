import datetime

import pytz
from pytz import timezone
from rest_framework import status

from .models import Users, AuthToken, UserRole
from django.contrib import auth
from uuid import uuid4
from .serializer import *


def login(username, password):
    try:
        print(username)
        user = Users.objects.get(username=username)
        if user is not None:
            user_auth = auth.authenticate(username=username, password=password)
            if user_auth is not None:
                t = uuid4()
                if not AuthToken.objects.filter(users=user).exists():
                    token = AuthToken(
                        token=t,
                        users=user,
                        last_login=datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                    )
                    token.save()
                else:
                    authToken = AuthToken.objects.get(users=user)
                    authToken.token = t
                    authToken.last_login = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                    authToken.save()

                return {
                    'status': True,
                    'message': 'Logged in successfully',
                    'token': t,
                    'user_id': user.id
                }
            else:
                return {
                    'status': False,
                    'message': 'Authorization Failed'
                }
    except Users.DoesNotExist:
        return {'status': False, 'message': 'User not found'}


def create_account(request):
    try:
        response = {}
        if not Users.objects.filter(username=request.data.get('username')).exists():
            data = request.data
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('password2')
            fname = data.get('fname')
            lname = data.get('lname')
            user_role = UserRole.objects.get(role_id=1)
            if password == confirm_password:
                user = Users(username=username, fname=fname, lname=lname, user_role=user_role)
                user.set_password(password)
                user.save()
                response = {
                    'status': True,
                    'message': 'Account Created',
                    'data': UserSerializer(user).data
                }
            else:
                response = {
                    'status': False,
                    'message': 'Password and Confirm Password does not match'
                }
        else:
            response = {
                'status': False,
                'message': 'User already exist'
            }
        return response
    except Exception as e:
        print(e)
        return {
            'status': False,
            'message': 'Internal server error'
        }
    except KeyError as e:
        return {
            'status': False,
            'message': str(e)
        }


def logout(token):
    try:
        token = AuthToken.objects.get(token=token)
        token.delete()
        return {
            'status': True,
            'message': 'Logout success'
        }
    except AuthToken.DoesNotExist:
        return {
            'status': False,
            'message': 'No login info found, already logged out'
        }


def get_profile(token):
    try:
        tokenObj = AuthToken.objects.get(token=token)
        user = Users.objects.get(id=tokenObj.users)
        return {
            'status': True,
            'data': user.__dict__
        }
    except AuthToken.DoesNotExist:
        return {
            'status': True,
            'message': 'Invalid Token'
        }
    except Users.DoesNotExist:
        return {
            'status': True,
            'message': 'Invalid User'
        }


def get_session_info(token):
    try:
        tokenObj = AuthToken.objects.get(token=token)
        return {
            'status': True,
            'data': TokenSerializer(tokenObj).data
        }
    except AuthToken.DoesNotExist:
        return {
            'status': False,
            'message': 'Invalid Token'
        }


def validate_login(token, renew):
    try:
        token = AuthToken.objects.get(token=token)
        curr = datetime.datetime.now()
        logout_date = token.last_login + datetime.timedelta(hours=token.validity)
        if curr >= logout_date:
            if not renew:
                token.delete()
                return {
                    'status': False,
                    'message': 'You have been logged out !'
                }
            else:
                t = uuid4()
                user = Users.objects.get(id=token.users.id)
                authToken = AuthToken.objects.get(users=user)
                authToken.token = t
                authToken.last_login = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                authToken.save()
                return {
                    'status': True,
                    'message': 'Your token has renewed, enjoy!'
                }
        else:
            return {
                'status': True,
                'message': 'Expiry date is too far'
            }
    except AuthToken.DoesNotExist as ae:
        return {
            'status': False,
            'message': 'Invalid token'
        }
    except Users.DoesNotExist:
        return {
            'status': False,
            'message': 'Invalid User'
        }


def get_token_user(token):
    try:
        token = AuthToken.objects.get(token=token)
        user = Users.objects.get(id=token.users.id)
        response = {
            'status': True,
            'data': UserSerializer(user).data
        }
    except Users.DoesNotExist:
        response = {
            'status': False,
            'message': "User doesn't exist"
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'message': "Token is invalid"
        }
    return response


def get_user(user_info, token):
    try:
        data = []
        AuthToken.objects.get(token=token)
        if Users.objects.filter(username=user_info).exists():
            data = UserSerializer(Users.objects.filter(username=user_info).get()).data
        elif Users.objects.filter(id=user_info).exists():
            data = UserSerializer(Users.objects.filter(id=user_info).get()).data
        response = {
            'status': len(data) > 0,
            'code': status.HTTP_200_OK if len(data) > 0 else status.HTTP_404_NOT_FOUND,
            'data': data,
            'params': user_info
        }
    except AuthToken.DoesNotExist:
        return {
            'status': False,
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Invalid or Expired Key'
        }
    except Users.DoesNotExist:
        return {
            'status': False,
            'code': status.HTTP_404_NOT_FOUND,
            'message': 'User not found'
        }
    except Exception as e:
        return {
            'status': False,
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'BAD REQUEST FORMAT'
        }
    return response


