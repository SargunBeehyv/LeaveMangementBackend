from rest_framework import serializers
from slmsapp.models import CustomUser, Staff, Staff_Leave


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()

    class Meta:
        model = Staff
        fields = "__all__"


class StaffLeaveSerializer(serializers.ModelSerializer):
    staff_first_name = serializers.CharField(
        source='staff_id.admin.first_name', read_only=True)

    class Meta:
        model = Staff_Leave
        fields = ['id', 'staff_id', 'staff_first_name', 'leave_type', 'status',
                  'message', 'from_date', 'created_at', 'to_date']
