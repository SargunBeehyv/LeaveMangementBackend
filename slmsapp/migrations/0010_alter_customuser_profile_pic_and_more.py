# Generated by Django 5.0.6 on 2024-07-16 04:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slmsapp', '0009_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(
                blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.IntegerField(
                choices=[(1, 'admin'), (2, 'staff')], default=2),
        ),
        migrations.AlterField(
            model_name='staff',
            name='admin',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='staff',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='staff_leave',
            name='from_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='staff_leave',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='leave_requests', to='slmsapp.staff'),
        ),
        migrations.AlterField(
            model_name='staff_leave',
            name='to_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='staff_leave',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
