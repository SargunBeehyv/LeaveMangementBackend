
from django.shortcuts import render, redirect, HttpResponse
from rest_framework.views import APIView
from slmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from slmsapp.models import CustomUser, Staff, Staff_Leave
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer, StaffSerializer, StaffLeaveSerializer
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from slmsapp.models import Staff, Staff_Leave
from django.contrib.auth.models import User


def dashboard_data(request):
    total_employees = Staff.objects.count()
    employees_on_leave = Staff_Leave.objects.filter(status=1).count()

    data = {
        'totalEmployees': total_employees,
        'employeesOnLeave': employees_on_leave,
    }
    return JsonResponse(data)


def employees_list(request):
    employees = Staff.objects.all()
    employees_data = [
        {
            'id': employee.admin.id,
            'fullName': f"{employee.admin.first_name} {employee.admin.last_name}",
            'username': employee.admin.username,
            'email': employee.admin.email,
            'gender': employee.gender,
            'joiningDate': employee.admin.date_joined.strftime('%Y-%m-%d'),
        }
        for employee in employees
    ]
    return JsonResponse(employees_data, safe=False)


@csrf_exempt
def delete_employee(request, employee_id):
    try:
        employee = CustomUser.objects.get(id=employee_id)
        employee.delete()
        return HttpResponse(status=204)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def approve_leave_request(request, request_id):
    try:
        leave_request = Staff_Leave.objects.get(id=request_id)
        leave_request.status = 'approved'
        leave_request.save()
        return HttpResponse(status=204)
    except Staff_Leave.DoesNotExist:
        return HttpResponse(status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reject_leave_request(request, request_id):
    try:
        leave_request = Staff_Leave.objects.get(id=request_id)
        leave_request.status = 'rejected'
        leave_request.save()
        return HttpResponse(status=204)
    except Staff_Leave.DoesNotExist:
        return HttpResponse(status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_staff(request):
    staff = Staff.objects.all()
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def edit_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    serializer = StaffSerializer(staff)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_staff(request):
    data = request.data
    user = get_object_or_404(CustomUser, id=data['staff_id'])
    user.username = data['username']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']

    if data['password']:
        user.set_password(data['password'])
    if data.get('profile_pic'):
        user.profile_pic = data['profile_pic']
    user.save()

    staff = get_object_or_404(Staff, admin=user)
    staff.address = data['address']
    staff.gender = data['gender']
    staff.save()
    return Response({'success': 'Staff updated successfully'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_staff(request, admin):
    user = get_object_or_404(CustomUser, id=admin)
    user.delete()
    return Response({'success': 'Staff deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_leave_view(request):
    leaves = Staff_Leave.objects.all()
    serializer = StaffLeaveSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def staff_approve_leave(request, id):
    leave = get_object_or_404(Staff_Leave, id=id)
    leave.status = 1
    leave.save()
    return Response({'success': 'Leave approved successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def staff_disapprove_leave(request, id):
    leave = get_object_or_404(Staff_Leave, id=id)
    leave.status = 2
    leave.save()
    return Response({'success': 'Leave disapproved successfully'})
