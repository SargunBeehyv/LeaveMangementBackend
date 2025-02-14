
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, staffviews, adminviews
from slmsapp import adminAPIveiws
from django.urls import path

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/login/', views.views_Login, name='views_Login'),
    path('api/logout/', views.logout_user, name='logout'),
    path('api/leave-history/', staffviews.get_leave_history, name='leave_history'),
    path('api/apply-leave/', staffviews.apply_leave, name='apply_leave'),
    path('api/dashboard/', staffviews.get_dashboard_data, name='dashboard'),
    path('api/user/profile/', staffviews.get_logged_in_user_details,
         name='user-profile'),

    path('api/employees/', adminviews.employees_list, name='employees_list'),
    path('api/employees/<int:employee_id>/',
         adminviews.delete_employee, name='delete_employee'),

    path('api/set_csrf_token/', adminAPIveiws.set_csrf_token),
    path('api/home/', adminAPIveiws.home, name='home'),
    path('api/add_staff/', adminAPIveiws.add_staff, name='add_staff'),
    path('api/view_staff/', adminAPIveiws.view_staff, name='view_staff'),
    path('api/staff_leave_view/', adminAPIveiws.staff_leave_view,
         name='staff_leave_view'),
    path('api/staff_approve_leave/<int:id>/',
         adminAPIveiws.staff_approve_leave, name='staff_approve_leave'),
    path('api/staff_disapprove_leave/<int:id>/',
         adminAPIveiws.staff_disapprove_leave, name='staff_disapprove_leave'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
