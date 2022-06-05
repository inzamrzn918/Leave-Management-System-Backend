import datetime
from lib2to3.pgen2 import token
from django.db.models import *
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserRole(Model):
    role_id = AutoField(primary_key=True)
    role_title = TextField(max_length=50, null=True, blank=False)


class Users(AbstractUser):
    id = AutoField(primary_key=True)
    fname = TextField(max_length=50, null=True, blank=True)
    lname = TextField(max_length=50, null=True, blank=True)
    username = TextField(max_length=50, null=False, blank=False, unique=True)
    password = TextField(max_length=500, null=False, blank=False)
    user_role = ForeignKey(UserRole, on_delete=SET_NULL, null=True, default=1)
    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(null=True)
    status = BooleanField(default=True)
    logical_delete = BooleanField(default=False)


class ProjectDetails(Model):
    pid = AutoField(primary_key=True)
    pname = TextField(max_length=250, blank=True, null=True)


class AuthToken(Model):
    token = TextField(max_length=1000, blank=False, null=False)
    created_at = DateTimeField(auto_now_add=True)
    users = ForeignKey(Users, on_delete=CASCADE)
    validity = IntegerField(default=24)
    last_login = DateTimeField(null=True)
