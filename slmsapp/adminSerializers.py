from rest_framework import serializers
from slmsapp.models import CustomUser, Staff, Staff_Leave


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email',
                  'username', 'profile_pic', 'user_type']


class StaffSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()

    class Meta:
        model = Staff
        fields = ['id', 'admin', 'address', 'gender']


class StaffLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff_Leave
        fields = ['staff_id', 'leave_type',
                  'from_date', 'to_date', 'message', 'created_at']
