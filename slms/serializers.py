# serializers.py
from rest_framework import serializers
from slmsapp.models import CustomUser, Staff, Staff_Leave


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_pic']


class StaffSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer()

    class Meta:
        model = Staff
        fields = '__all__'


class StaffLeaveSerializer(serializers.ModelSerializer):
    staff_id = StaffSerializer()

    class Meta:
        model = Staff_Leave
        fields = '__all__'
