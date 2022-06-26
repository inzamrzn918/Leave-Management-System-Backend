from datetime import timezone
from itertools import count
from rest_framework import status

from .serializer import *


def get_leaves_by_token(token):
    try:
        leaves_record = {}
        token = AuthToken.objects.get(token=token)
        user = Users.objects.get(id=token.users.id)
        if user.user_role_id == 2:
            manager = Manager.objects.get(mid=user.id)
            emps = Employee.objects.filter(rep_manager_id_id=manager.id)
            req_leaves = []
            for emp in emps:
                ls = RequestedLeaves.objects.filter(eid_id=emp.eid)
                req_leaves.append(ls)
        elif user.user_role_id == 3:
            req_leaves = RequestedLeaves.objects.all()
        else:
            employee = Employee.objects.get(user_id=user.id)
            req_leaves = RequestedLeaves.objects.filter(eid=employee.eid).all()
        req = []
        app = []
        for rl in req_leaves:
            rcby = None
            if Leaves.objects.filter(request=rl.request_id).exists():
                lo = Leaves.objects.get(request=rl.request_id)
                if lo.request.status != 'deleted' and rl.status != 'approved' and rl.status != 'rejected' and  (rl.request_date>=datetime.datetime.now(timezone.utc)):
                    app.append({
                        "title": f'{user.fname} - {lo.request.reason}',
                        "reason": rl.reason,
                        "description": '',
                        "start": lo.request.request_date,
                        "end": lo.request.request_date + datetime.timedelta(days=lo.request.duration-1),
                        "leave_data": LeavesSerializer(lo).data,
                        "leave_req_data": RequestLeaveSerializer(lo.request),
                        "backgroundColor": "red" if lo.request.status == 'rejected'
                        else 'green' if lo.request.status == 'approved' else 'blue'
                        if rl.eid.user_id_id != user.id else "red",
                        "applier": lo.request.eid.user_id_id
                    })

            else:
                # req.append(RequestLeaveSerializer(rl).data)
                if rl.status != 'deleted' and rl.status != 'approved' and rl.status != 'rejected'  and (rl.request_date>=datetime.datetime.now(timezone.utc)):
                    req.append({
                        "title": f'{user.fname} - {rl.reason}',
                        "reason": rl.reason,
                        "description": '',
                        "start": rl.request_date,
                        "end": rl.request_date + datetime.timedelta(days=rl.duration-1),
                        "leave_req_data": RequestLeaveSerializer(rl).data,
                        "leave_data": None,
                        "backgroundColor": "blue" if rl.eid.user_id_id != user.id else "red",
                        "applier": rl.eid.user_id_id

                    })
        leaves_record['requested'] = req
        leaves_record['approved'] = app
        response = {
            'status': True,
            'data': leaves_record
        }

    except AuthToken.DoesNotExist as e:
        response = {
            'status': False,
            'message': 'Invalid Token'
        }
    except Users.DoesNotExist as f:
        response = {
            'status': False,
            'message': 'User not found'
        }
    except Employee.DoesNotExist as g:
        response = {
            'status': False,
            'message': 'Not an Employee'
        }
    return response


def manager_leaves(token):
    try:
        leaves_record = {}
        token = AuthToken.objects.get(token=token)
        user = Users.objects.get(id=token.users.id)
        manager = Manager.objects.get(user_id=user.id)
        employee = Employee.objects.get(user_id=user.id)
        req_leaves = RequestedLeaves.objects.filter(eid=employee.eid).all()
        for rl in req_leaves:
            ob = Leaves.objects.filter(approved_by=manager.id)
            if ob.exists():
                leaves_record['approved'] = LeavesSerializer(ob.get()).data
            else:
                leaves_record['requested'] = RequestLeaveSerializer(rl).data
        response = {
            'status': True,
            'data': leaves_record
        }
    except AuthToken.DoesNotExist as e:
        response = {
            'status': False,
            'message': 'Invalid Token'
        }
    except Users.DoesNotExist as f:
        response = {
            'status': False,
            'message': 'User not found'
        }
    except Employee.DoesNotExist as g:
        response = {
            'status': False,
            'message': 'Not an Employee'
        }
    except Manager.DoesNotExist as m:
        response = {
            'status': False,
            'message': 'Not an Manager'
        }
    return response


def request_leave(token, body):
    try:
        token = AuthToken.objects.get(token=token)
        employee = Employee.objects.get(user_id_id=token.users_id)
        date = datetime.datetime.strptime(body['start'], "%Y-%m-%d")
        print(body['type'])
        if not RequestedLeaves.objects.filter(request_date=date, status='requested', eid = employee).exists():
            req_leave = RequestedLeaves(eid_id=employee.eid, status='requested', request_date=date,
                                        reason=body['reason'], duration=body['duration'], leave_type_id=body['type'])
            employee.total_leaves -= body['duration']
                
            req_leave.save()
            employee.save()

            response = {
                'status': True,
                'message': f'''Requested leave for {req_leave.duration} days on {req_leave.request_date}''',
                'code': status.HTTP_201_CREATED
            }
        else:
            response = {
                'status': False,
                'message': 'You can not apply twich on same date',
                'code': status.HTTP_404_NOT_FOUND
            }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'message': 'Invalid token',
            'code': status.HTTP_404_NOT_FOUND
        }
    except Employee.DoesNotExist:
        response = {
            'status': False,
            'message': 'You are not an employee',
            'code': status.HTTP_404_NOT_FOUND
        }
    except Exception as e:
        print(body)
        response = {
            'status': False,
            'message': str(e),
            'code': status.HTTP_400_BAD_REQUEST
        }
    return response


def delete_leaves_requeste(token, id):
    try:
        token = AuthToken.objects.get(token=token)
        if Leaves.objects.filter(leave_id=id).exists():
            leave = Leaves.objects.get(leave_id=id)
            lr = RequestedLeaves.objects.get(request_id=leave.request_id)
        else:
            lr = RequestedLeaves.objects.get(request_id=id)
        lr.status = 'deleted'
        lr.save()
        response = {
            'status': True,
            'message': 'Deleted!',
            'code': 200
        }
    except AuthToken.DoesNotExist:
        response = {
            'status': False,
            'message': 'Invalid Token',
            'code': status.HTTP_400_BAD_REQUEST
        }
    except RequestedLeaves.DoesNotExist:
        response = {
            'status': False,
            'message': 'Leave details not found',
            'code': 404
        }
    return response


def get_leaves(token, request_id):
    try:
        token = AuthToken.objects.get(token=token)
        emp = Employee.objects.get(user_id=token.users)
        if token.users.id == 3:
            lr = RequestLeaveSerializer(RequestedLeaves.objects.get(request_id=request_id)).data
        elif token.users.id == 2:
            lcs = RequestedLeaves.objects.get(request_id=request_id)
            if lcs.eid.rep_manager_id == token.users:
                lr = RequestLeaveSerializer(lcs).data
            else:
                lr = None
        else:
            lcs = RequestedLeaves.objects.get(request_id=request_id, eid=emp)
            lr = RequestLeaveSerializer(lcs).data

        if lr is None:
            response = {
                'status': False,
                'message': "You are not manager of the employee",
                'code': status.HTTP_401_UNAUTHORIZED
            }
        else:
            response = {
                'status': True,
                'data': lr,
                'code': status.HTTP_200_OK
            }
    except (AuthToken.DoesNotExist, Employee.DoesNotExist, RequestedLeaves.DoesNotExist,
            Leaves.DoesNotExist) as e:
        response = {
            'status': False,
            'message': 'Not found',
            'code': status.HTTP_404_NOT_FOUND
        }

    return response


def update_leave(token, body):
    try:
        token = AuthToken.objects.get(token=token)
        ls = RequestedLeaves.objects.get(request_id=body['request_id'])
        ls.status = body['status']
        ls.save()
        response = {
            'status': True,
            'message': "Leave request " + body['status'],
            'code': status.HTTP_201_CREATED
        }
    except (AuthToken.DoesNotExist, RequestedLeaves.DoesNotExist) as e:
        response = {
            'status': False,
            'message': 'Not found',
            'code': status.HTTP_404_NOT_FOUND
        }
    return response

def get_types(token):
    try:
        token = AuthToken.objects.get(token=token)
        lt = LeaveType.objects.all()
        lt = LeaveTypeSerializer(lt, many=True)
        response = {
            'status':True,
            'message':'Success',
            'data':lt.data,
            'code':status.HTTP_200_OK
        }
    except Exception as e:
        response = {
            'status':False,
            'code':status.HTTP_400_BAD_REQUEST,
            'message':str(e)
        }
    return response


def set_types(token, body):
    try:
        token = AuthToken.objects.get(token=token)
        if not LeaveType.objects.filter(title=body['title']).exists():
            lt = LeaveType(title=body['title'], max_amount=body['count'])
            lt.save()
            response = {
                'status':True,
                'message':'Saved Successfully',
                'code':status.HTTP_200_OK
            }
        else:
            response = {
                'status':False,
                'message':'Alredy Exist',
                'code':status.HTTP_406_NOT_ACCEPTABLE
            }
    except Exception as e:
        response = {
            'status':False,
            'code':status.HTTP_400_BAD_REQUEST,
            'message':str(e)
        }
    return response

def update_type(token, body):
    try:
        token = AuthToken.objects.get(token=token)
        if LeaveType.objects.filter(body).exists():
            lt = LeaveType.objects.get(body)
            lt.title = body['title']
            lt.save()
            response = {
                'status':True,
                'message':'Updated Successfully',
                'code':status.HTTP_200_OK
            }
        else:
            response = {
                'status':False,
                'message':'Not Exist',
                'code':status.HTTP_304_NOT_MODIFIED
            }
    except Exception as e:
        response = {
            'status':False,
            'code':status.HTTP_400_BAD_REQUEST,
            'message':str(e)
        }
    return response 

def get_leave_balance(token):
    try:
        token = AuthToken.objects.get(token=token)
        employee = Employee.objects.get(user_id=token.users)
        lr = RequestedLeaves.objects.filter(status='requested',eid=employee)
        lb = employee.total_leaves
        for lrc in lr:
            lb -= lrc.leave_type.max_amount
        response = {
            'status':True,
            'code':status.HTTP_200_OK,
            'lb':lb,
            'cpl':employee.ctc/365
        }
    
    except Exception as e:
        response = {
            'status':False,
            'code':status.HTTP_400_BAD_REQUEST,
            'message':str(e)
        }
    return response