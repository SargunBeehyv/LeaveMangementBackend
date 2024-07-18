# Generated by Django 5.0.6 on 2024-07-12 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slmsapp', '0008_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(
                choices=[(1, 'admin'), (2, 'staff')], default=1, max_length=50),
        ),
    ]
