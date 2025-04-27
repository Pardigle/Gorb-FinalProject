from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip

# Create your views here.
def employees_page(request):
    employees = Employee.objects.all()
    return render(request, 'payroll_app/employees_page.html', {'employees':employees})

def payslips_page(request):
    payslips = Payslip.objects.all()
    return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips})

def create_employee(request):
    return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'payroll_app/update_employee.html', {'employee':employee})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/view_payslip.html', {'payslip':payslip})