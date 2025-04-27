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
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    payslips = Payslip.objects.all().order_by('-year', '-month_integer_reference', '-pay_cycle')
    employees = Employee.objects.all()
    if (request.method=="POST"):
        button = request.POST.get("button")

        if button == "search":
            creds = request.POST.get("Search")
            employee = Employee.objects.filter(id_number=creds)
            if employee:
                payslips = Payslip.objects.filter(id_number=employee[0]).order_by('-year', 'month_integer_reference', 'pay_cycle')
            return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months})
        
        elif button == "create":
            months_as_integers = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
            id_number = request.POST.get("employee")
            month = request.POST.get("month")
            year = request.POST.get("year")
            cycle = int(request.POST.get("cycle"))
            employee = Employee.objects.get(id_number=id_number)
            month_integer_reference = months_as_integers[month]
            
            if Payslip.objects.filter(id_number=employee, month=month, year=year, pay_cycle=cycle).exists():
                return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months, 'message':'Payslip already exists!'})
            else:
                if cycle == 2:
                    date_range = '16-31' if month in ['January', 'March', 'May', 'August', 'October', 'December'] else '16-29' if (month == 'February' and (year%4==0 and (year%400==0 or year%100!=0))) else '16-28' if month=='February' else '16-30'
                    philhealth = employee.getRate() * 0.04
                    sss = employee.getRate() * 0.045
                    overtime = employee.getOvertime()
                    rate = employee.getRate()
                    allowance = employee.getAllowance()
                    deductions_tax = ((rate/2) + allowance + overtime - philhealth - sss) * 0.2
                    total_pay = ((rate/2) + allowance + overtime - philhealth - sss) - deductions_tax

                    Payslip.objects.create(id_number=employee, month=month, date_range=date_range, year=year, pay_cycle=cycle, rate=rate, earnings_allowance=allowance, deductions_tax=deductions_tax, deductions_health=philhealth, pag_ibig=0, sss=sss, overtime=overtime, total_pay=total_pay, month_integer_reference=month_integer_reference)
               
                elif cycle == 1:
                    date_range = '1-15'
                    overtime = employee.getOvertime()
                    rate = employee.getRate()
                    allowance = employee.getAllowance()
                    pag_ibig = 100
                    deductions_tax = ((rate/2) + allowance + overtime - pag_ibig) * 0.2
                    total_pay = ((rate/2) + allowance + overtime - pag_ibig) - deductions_tax

                    Payslip.objects.create(id_number=employee, month=month, date_range=date_range, year=year, pay_cycle=cycle, rate=rate, earnings_allowance=allowance, deductions_tax=deductions_tax, deductions_health=0, pag_ibig=pag_ibig, sss=0, overtime=overtime, total_pay=total_pay, month_integer_reference=month_integer_reference)
                
                payslips = Payslip.objects.all().order_by('-year', '-month_integer_reference', '-pay_cycle')
                employees = Employee.objects.all()
                Employee.objects.filter(id_number=id_number).update(overtime_pay=0)
                return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months, 'message':'Payslip successfully created!'})
    else:
        return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months})

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
    base = payslip.id_number.getRate() / 2
    gross_pay = base + payslip.id_number.getAllowance() + payslip.getOvertime()
    total_deductions = payslip.getDeductions_tax() + payslip.getDeductions_health() + payslip.getSSS() + payslip.getPag_ibig()
    return render(request, 'payroll_app/view_payslip.html', {'payslip':payslip, 'base':base, 'gross':gross_pay, 'deduction':total_deductions})