from django.db.models import *
from core.models import *
from employee.models import *


class LeaveType(Model):
    title = CharField(max_length=50, null=False, blank=False)
    
class UserLeaveCount(Model):
    user = ForeignKey(Users, on_delete=CASCADE, null=False, blank=False)
    leave_type = ForeignKey(LeaveType, on_delete=CASCADE, null=False,blank=False)
    count = FloatField()
    

class RequestedLeaves(Model):
    request_id = AutoField(primary_key=True)
    eid = ForeignKey(Employee, on_delete=CASCADE)
    status = TextField(max_length=15, blank=False, null=False, default='requested')
    request_date = DateTimeField(null=False, blank=False)
    reason = TextField(max_length=250, blank=True, null=True)
    duration = FloatField(null=False, default=1)
    leave_type = ForeignKey(LeaveType, on_delete=CASCADE, null=True)


class Leaves(Model):
    leave_id = AutoField(primary_key=True)
    request = ForeignKey(RequestedLeaves, on_delete=CASCADE)
    paid_unpaid = BooleanField(default=False)
    approved_by = ForeignKey(Manager, on_delete=SET_NULL, null=True)
    approved_time = DateTimeField(auto_now_add=True)
    # end_date = DateTimeField(null=False)
