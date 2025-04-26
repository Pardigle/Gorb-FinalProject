from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employees_page, name='employees'),
    path('payslips', views.payslips_page,  name='payslips'),
    path('create_employee', views.create_employee,  name='create_employee'),
    path('update_employee/<int:pk>', views.update_employee,  name='update_employee'),
    path('payslips/<int:pk>', views.view_payslip,  name='view_payslip'),

]