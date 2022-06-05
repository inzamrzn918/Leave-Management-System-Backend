import datetime

from .serializer import *
from rest_framework import status


def get_leaves_by_token(token):
    try:
        leaves_record = {}
        token = AuthToken.objects.get(token=token)
        user = Users.objects.get(id=token.users.id)
        employee = Employee.objects.get(user_id=user.id)
        req_leaves = RequestedLeaves.objects.filter(eid=employee.eid).all()
        req = []
        app = []
        for rl in req_leaves:
            if Leaves.objects.filter(request=rl.request_id).exists():
                lo = Leaves.objects.get(request=rl.request_id)
                if lo.request.status != 'deleted':
                    app.append({
                        "title": lo.request.reason,
                        "description": '',
                        "start": lo.request.request_date,
                        "end": lo.request.request_date + datetime.timedelta(days=lo.request.duration),
                        "leave_data": LeavesSerializer(lo).data,
                        "leave_req_data": RequestLeaveSerializer(lo.request),
                        "backgroundColor": "red" if lo.request.status == 'rejected'
                        else 'green' if lo.request.status == 'approved' else 'blue '
                    })

            else:
                # req.append(RequestLeaveSerializer(rl).data)
                if rl.status!='deleted':
                    req.append({
                        "title": rl.reason,
                        "description": '',
                        "start": rl.request_date,
                        "end": rl.request_date + datetime.timedelta(days=rl.duration),
                        "leave_req_data": RequestLeaveSerializer(rl).data,
                        "leave_data": None,
                        "backgroundColor": "blue"
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
        # print(body['start'], date)
        req_leave = RequestedLeaves(eid_id=employee.eid, status='requested', request_date=date,
                                    reason=body['reason'], duration=body['duration'])
        req_leave.save()

        response = {
            'status': True,
            'message': f'''Requested leave for {req_leave.duration} days on {req_leave.request_date}''',
            'code': status.HTTP_201_CREATED
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
        response = {
            'status': False,
            'message': str(e),
            'code': status.HTTP_400_BAD_REQUEST,
            'body': body

        }
    return response


def approve_leaves(token, req_id, paid=False, duration=None):
    try:
        token = AuthToken.objects.get(token=token)
        manager = Manager.objects.get(user_id=token.users)
        lrs = RequestedLeaves.objects.get(request_id=req_id)
        endtime = datetime.datetime.now() + datetime.timedelta(hours=duration * 24)
        leavobj = Leaves(request_id=lrs.request_id, paid_unpaid=paid, approved_by=manager.id, end_date=str(endtime))
        leavobj.save()
        lrs.status = "approved"
        if duration is not None:
            lrs.duration = duration
        lrs.save()
        response = {
            'status': True,
            'message': f'''Leave approved for {lrs.duration} days'''
        }

    except Manager.DoesNotExist:
        response = {
            'status': False,
            'message': 'You are not a manager',
            'code': status.HTTP_400_BAD_REQUEST
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
            'message': 'Invalid Leave Id',
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