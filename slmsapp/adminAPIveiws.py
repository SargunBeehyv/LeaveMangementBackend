from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from slmsapp.models import CustomUser, Staff, Staff_Leave
from slmsapp.adminSerializers import CustomUserSerializer, StaffSerializer, StaffLeaveSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse


@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    staff_count = Staff.objects.count()
    leave_count = Staff_Leave.objects.count()
    context = {
        'staff_count': staff_count,
        'leave_count': leave_count
    }
    return Response(context)


@api_view(['POST'])
def add_staff(request):
    data = request.data
    if CustomUser.objects.filter(email=data['email']).exists():
        return Response({'detail': 'Email is already Exist'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(username=data['username']).exists():
        return Response({'detail': 'Username is already Exist'}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        profile_pic=data['profilePhoto'],
        user_type=2,
        username=data['username']
    )
    user.set_password(data['password'])
    user.save()

    staff = Staff(
        admin=user,
        address="HYD",
        gender=data['gender']
    )
    staff.save()

    return Response({'detail': 'Staff details have been added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_staff(request):
    staff = Staff.objects.all()
    serializer = StaffSerializer(staff, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def edit_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    serializer = StaffSerializer(staff)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_staff(request, admin):
    staff = get_object_or_404(CustomUser, id=admin)
    staff.delete()
    return Response({'detail': 'Staff record has been deleted successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_leave_view(request):
    if request.user.user_type == 1:  # Assuming user_type 1 is for admin
        staff_leave = Staff_Leave.objects.all()
    else:
        staff_leave = Staff_Leave.objects.filter(staff_id=request.user.staff)
    serializer = StaffLeaveSerializer(staff_leave, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def staff_approve_leave(request, id):
    if request.user.user_type == 1:  # Only admin can approve leave
        leave = get_object_or_404(Staff_Leave, id=id)
        leave.status = 1
        leave.save()
        serializer = StaffLeaveSerializer(leave)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'You are not authorized to approve leave'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def staff_disapprove_leave(request, id):
    if request.user.user_type == 1:  # Only admin can disapprove leave
        leave = get_object_or_404(Staff_Leave, id=id)
        leave.status = 2
        leave.save()
        serializer = StaffLeaveSerializer(leave)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'You are not authorized to disapprove leave'}, status=status.HTTP_403_FORBIDDEN)
