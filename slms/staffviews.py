
from slmsapp.models import Staff, Staff_Leave
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StaffLeaveSerializer, CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leave_history(request):
    staff = Staff.objects.get(admin=request.user.id)
    leaves = Staff_Leave.objects.filter(staff_id=staff.id)
    serializer = StaffLeaveSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_leave(request):
    data = request.data
    staff = Staff.objects.get(admin=request.user.id)
    leave = Staff_Leave.objects.create(
        staff_id=staff,
        leave_type=data['leaveType'],
        from_date=data['startDate'],
        to_date=data['endDate'],
        message=data['reason'],
    )
    leave.save()
    print("Leave saved ")
    return Response({'success': 'Leave applied successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_data(request):
    staff = Staff.objects.get(admin=request.user.id)
    leaves = Staff_Leave.objects.filter(staff_id=staff.id)
    serializer = StaffLeaveSerializer(leaves, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user_details(request):
    user = request.user
    serializer = CustomUserSerializer(user)
    return Response(serializer.data)
