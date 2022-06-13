from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import *


class LeavesSerializer(ModelSerializer):
    applied_leave_id = serializers.RelatedField(source="AppliedLeaves", read_only=True)
    approved_by = serializers.RelatedField(source="employee.models.Manager", read_only=True)

    class Meta:
        model = Leaves
        fields = ('leave_id', 'applied_leave_id', 'paid_unpaid', 'approved_by', 'approved_time')


class RequestLeaveSerializer(ModelSerializer):
    eid = serializers.RelatedField(source="employee.models.Employee", read_only=True)

    class Meta:
        model = RequestedLeaves
        fields = ['request_id', 'eid', 'status', 'request_date', 'reason', 'duration']
        
class LeaveTypeSerializer(ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
