from django.urls import path
from .views import *

urlpatterns = [
    path('my_leaves', view=my_leaves),
    path('apply', view=request_leave),
    path('delete', view=delete_leave),

]

