from django.db import models
from django.contrib.auth.models import AbstractUser


from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_CHOICES = (
        (1, 'admin'),
        (2, 'staff'),
    )
    user_type = models.IntegerField(choices=USER_CHOICES, default=2)
    profile_pic = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username


class Staff_Leave(models.Model):
    staff_id = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    message = models.TextField()
    # 0: Pending, 1: Approved, 2: Not Approved
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff_id.admin.username}'s {self.leave_type} Leave"
