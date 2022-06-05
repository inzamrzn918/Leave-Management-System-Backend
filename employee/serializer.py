from django.db.models.fields.related import RelatedField
from rest_framework.serializers import ModelSerializer
from .models import *
from core.serializer import *


class ManagerSerializer(ModelSerializer):
    user_id = UserDataSerializer()

    # name = "user_id.fname"

    class Meta:
        model = Manager
        fields = ['mid', 'user_id']


class EmployeeSerializer(ModelSerializer):
    user_id = UserSerializer()
    rep_manager_id = ManagerSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class DeptSeriaizer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class HardwareSerializer(ModelSerializer):
    eid = EmployeeSerializer()

    class Meta:
        model = Department
        fields = '__all__'
