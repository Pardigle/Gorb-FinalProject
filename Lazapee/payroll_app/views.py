from django.shortcuts import render
from models import Employee, Payslip

# Create your views here.
def employees_page(request):
    employees = Employee.objects.all()
    return render(request, 'payroll_app/employees_page.html', {'employees':employees})

