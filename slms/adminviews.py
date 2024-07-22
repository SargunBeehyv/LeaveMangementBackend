from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import HttpResponse
from slmsapp.models import CustomUser, Staff
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_employee(request, employee_id):
    try:
        employee = CustomUser.objects.get(id=employee_id)
        employee.delete()
        return HttpResponse(status=204)
    except CustomUser.DoesNotExist:
        return HttpResponse(status=404)
