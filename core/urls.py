from xml.etree.ElementInclude import include
from django.urls import path, include
from .views import *


urlpatterns = [
    path('login', view=login),
    path('create_account', view=create_account),
    # path('forgot_password/', view=login),
    path('account', view=my_account),
    path('logout', view=logout),
    path('session_info', view=session_info),
    path('get_token_user', view=get_token_user),
    path('onboard', view=onboard),
    path('get_user', view=get_user),
    path('password_validation', view=password_validation),

]
