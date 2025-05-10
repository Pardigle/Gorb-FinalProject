from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login'), 
    path('signup/', views.signup_page, name='signup'),
    path('logout/', views.logout_page, name='logout'),
    path('account/<int:pk>', views.manage_account, name='manage_account'),
    path('account/<int:pk>/change_password', views.change_password, name='change_password'),
    path('account/<int:pk>/delete', views.delete_account, name='delete_account'),
    path('admin/', admin.site.urls),
    path('employees', views.employees_page, name='employees'),
    path('payslips', views.payslips_page,  name='payslips'),
    path('create_employee', views.create_employee,  name='create_employee'),
    path('update_employee/<int:pk>', views.update_employee,  name='update_employee'),
    path('payslips/<int:pk>', views.view_payslip,  name='view_payslip'),
    path('delete_employee/<int:pk>', views.delete_employee, name='delete_employee'),

]