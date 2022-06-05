from django.db.models import *

# Create your models here.
from core.models import Users, ProjectDetails


class Manager(Model):
    mid = AutoField(primary_key=True)
    user_id = ForeignKey(Users, on_delete=CASCADE, null=True)


class Department(Model):
    dept_id = AutoField(primary_key=True)
    dept_name = TextField(max_length=100, blank=True, null=True)


class Employee(Model):
    eid = AutoField(primary_key=True)
    user_id = ForeignKey(Users, on_delete=CASCADE, related_name="user_account_id")
    dept = ForeignKey(Department, on_delete=SET_NULL, null=True, blank=True)
    isConfirmed = BooleanField(default=True)
    isManager = BooleanField(default=False)
    experiance = TextField(max_length=250, blank=True, null=True)
    blood_group = TextField(max_length=20, blank=True, null=True)
    address = TextField(max_length=1024, blank=True, null=True)
    marital_status = TextField(max_length=25, blank=True, null=True)
    rep_manager_id = ForeignKey(Manager, on_delete=SET_NULL, null=True)
    contact_no = TextField(max_length=14, blank=True, null=True)
    dob = TextField(max_length=12, blank=True, null=True)
    kanaka_id = TextField(max_length=25, blank=True, null=True)
    total_leaves = IntegerField(null=False, default=21)
    remaining_leaves = IntegerField(null=False, default=21)
    onborded_by = ForeignKey(Users, on_delete=SET_NULL, null=True, related_name="created_by")

    def __str__(self):
        return self.eid


class ProjectEmployee(Model):
    pid = ForeignKey(ProjectDetails, on_delete=CASCADE)
    eid = ForeignKey(Employee, on_delete=CASCADE)
    date_of_join = DateTimeField(auto_now_add=True)


class HardwareDetails(Model):
    slno = IntegerField(primary_key=True)
    eid = ForeignKey(Employee, on_delete=CASCADE)
    proccessor = TextField(max_length=50, blank=True, null=False)
    hdd = TextField(max_length=50, blank=True, null=False)
    ram = TextField(max_length=50, blank=True, null=False)
    mfg_year = TextField(max_length=4, blank=True, null=False)
    os = TextField(max_length=50, blank=True, null=False)
    asset_code = TextField(max_length=50, blank=True, null=False)
    service_tag = TextField(max_length=50, blank=True, null=False)
