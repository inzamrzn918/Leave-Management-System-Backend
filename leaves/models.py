# Create your models here.
from django.db.models import *
from core.models import *
from employee.models import *


class RequestedLeaves(Model):
    request_id = AutoField(primary_key=True)
    eid = ForeignKey(Employee, on_delete=CASCADE)
    status = TextField(max_length=15, blank=False, null=False, default='APPLIED')
    request_date = DateTimeField(auto_now_add=True)
    reason = TextField(max_length=250, blank=True, null=True)
    duration = IntegerField(null=False, default=1)


class Leaves(Model):
    leave_id = AutoField(primary_key=True)
    request = ForeignKey(RequestedLeaves, on_delete=CASCADE)
    paid_unpaid = BooleanField(default=False)
    approved_by = ForeignKey(Manager, on_delete=SET_NULL, null=True)
    approved_time = DateTimeField(auto_now_add=True)
    # end_date = DateTimeField(null=False)
