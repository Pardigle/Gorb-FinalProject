from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip

# Create your views here.
def employees_page(request):
    if (request.method=="POST"):
        button = request.POST.get("button")

        if button == "search":
            creds = request.POST.get("Search")
            
            if creds.isdigit() == True:
                employees = Employee.objects.filter(id_number=creds)
                return render(request, 'payroll_app/employees_page.html', {'employees':employees})
            else:
                employees = Employee.objects.filter(name__icontains=creds)
                return render(request, 'payroll_app/employees_page.html', {'employees':employees})
        
        elif button == "add_overtime":
            id = request.POST.get("employee_id")
            hours = request.POST.get("hours")
            overtime = get_object_or_404(Employee, id_number=id).getOvertime() + (get_object_or_404(Employee, id_number=id).getRate()/160) * 1.5 * int(hours)
            Employee.objects.filter(id_number=id).update(overtime_pay=overtime)

            employees = Employee.objects.all()
            return render(request, 'payroll_app/employees_page.html', {'employees':employees})

    else:
        employees = Employee.objects.all()
        message = request.session.pop('message', None)
        return render(request, 'payroll_app/employees_page.html', {'employees':employees, 'message':message})

def payslips_page(request):
    payslips = Payslip.objects.all()
    return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips})

def create_employee(request):
    if (request.method=="POST"):
        button = request.POST.get("button")
        name = request.POST.get("name")
        rate = float(request.POST.get("rate"))
        id_number = int(request.POST.get("id_number"))
        allowance = request.POST.get("allowance")

        if button == "submit":
            if not allowance:
                Employee.objects.create(name=name, rate=rate, id_number=id_number, allowance=0, overtime_pay=0)
            else:
                Employee.objects.create(name=name, rate=rate, id_number=id_number, allowance=allowance, overtime_pay=0)
            request.session['message'] = "Employee created!"
            return redirect('employees')

    return render(request, 'payroll_app/create_employee.html')

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')

def update_employee(request, pk):
    if (request.method=="POST"):
        button = request.POST.get("button")
        name = request.POST.get("name")
        rate = float(request.POST.get("rate"))
        id_number = int(request.POST.get("id_number"))
        allowance = request.POST.get("allowance")

        if button == "submit":
            Employee.objects.filter(pk=pk).update(name=name, rate=rate, id_number=id_number, allowance=allowance)
            request.session['message'] = "Employee details updated!"
            return redirect('employees')
    else:
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html', {'employee':employee})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/view_payslip.html', {'payslip':payslip})