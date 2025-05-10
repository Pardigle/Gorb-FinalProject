from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip, Account

global history
global account
history = [] ##This is for an additional functionality where the user knows the 5 latest generated payslips.
account = '' # Globan Session Variable
    
def login_page(request):
    global account_id
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            account = Account.objects.get(username=username, password=password)
            return redirect('employees')
        except Account.DoesNotExist:
            return render(request, 'payroll_app/login.html', {'error': 'Invalid login'})
    return render(request, 'payroll_app/login.html')

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if Account.objects.filter(username=username).exists():
            return render(request, 'payroll_app/signup.html', {'error': 'Account already exists'})
        if password == "":
            return render(request, 'payroll_app/signup.html', {'error': 'Password cannot be blank'})
        Account.objects.create (username=username, password=password)
        return render(request, 'payroll_app/login.html', {'message': 'Account created successfully'})
    return render(request, 'payroll_app/signup.html')


def logout_page(request):
    global account
    account = ''
    return redirect('login')

def manage_account(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'payroll_app/manage_account.html', {'account': account})

def change_password(request, pk):
    account = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        old_pw = request.POST.get('old_pw')
        new_pw1 = request.POST.get('new_pw1')
        new_pw2 = request.POST.get('new_pw2')

        if old_pw != account.password:
            return render(request, 'payroll_app/change_password.html', {'account': account, 'error': 'Current password incorrect.'})
        if new_pw1 != new_pw2:
            return render(request, 'payroll_app/change_password.html', {'account': account, 'error': 'New passwords do not match.'})
        if new_pw1 == "" or new_pw2 == "":
            return render(request, 'payroll_app/change_password.html', {'account': account, 'error': 'New password cannot be empty.'})

        account.password = new_pw1
        account.save()
        return redirect('manage_account', pk=pk)

    return render(request, 'payroll_app/change_password.html', {'account': account})

def delete_account(request, pk):
    global account
    Account.objects.filter(pk=pk).delete()
    account = 0
    return redirect('login')

def employees_page(request):
    global history
    global account
    if (request.method=="POST"):
        button = request.POST.get("button")

        if button == "search":
            creds = request.POST.get("Search")
            
            if creds.isdigit() == True:
                employees = Employee.objects.filter(id_number=creds)
                return render(request, 'payroll_app/employees_page.html', {'employees':employees, 'history':history, 'account':account})
            else:
                employees = Employee.objects.filter(name__icontains=creds)
                return render(request, 'payroll_app/employees_page.html', {'employees':employees, 'history':history, 'account':account})
        
        elif button == "add_overtime":
            id = request.POST.get("employee_id")
            hours = request.POST.get("hours")
            overtime = get_object_or_404(Employee, id_number=id).getOvertime() + (get_object_or_404(Employee, id_number=id).getRate()/160) * 1.5 * int(hours)
            Employee.objects.filter(id_number=id).update(overtime_pay=overtime)

            employees = Employee.objects.all()
            return render(request, 'payroll_app/employees_page.html', {'employees':employees, 'history':history, 'account':account})

    else:
        employees = Employee.objects.all()
        message = request.session.pop('message', None)
        return render(request, 'payroll_app/employees_page.html', {'employees':employees, 'message':message, 'history':history, 'account':account})

def payslips_page(request):
    global history
    global account
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    payslips = Payslip.objects.all().order_by('-pk')
    employees = Employee.objects.all()
    if (request.method=="POST"):
        button = request.POST.get("button")
        sorting = request.POST.get("sort")

        if button == "search":
            creds = request.POST.get("Search")
           
            if ":" in creds:
                creds = creds.upper().split(":")
                if "BEFORE" in creds:
                    if len(creds) > 1:
                        if len(creds[1]) == 2 and creds[1].isdigit():
                            if len(creds[2]) == 4 and creds[2].isdigit():
                                payslips = Payslip.objects.filter(month_integer_reference__lte=int(creds[1]), year__lte=int(creds[2])).order_by('-year', 'month_integer_reference', 'pay_cycle')
                            else:
                                payslips = Payslip.objects.filter(month_integer_reference__lte=int(creds[1])).order_by('-year', 'month_integer_reference', 'pay_cycle')
                        elif len(creds[1]) == 4 and creds[1].isdigit():
                            payslips = Payslip.objects.filter(year__lte=int(creds[1]))
                elif "AFTER" in creds:
                    if len(creds) > 1:
                        if len(creds[1]) == 2 and creds[1].isdigit():
                            if len(creds[2]) == 4 and creds[2].isdigit():
                                payslips = Payslip.objects.filter(month_integer_reference__gte=int(creds[1]), year__gte=int(creds[2])).order_by('-year', 'month_integer_reference', 'pay_cycle')
                            else:
                                payslips = Payslip.objects.filter(month_integer_reference__gte=int(creds[1])).order_by('-year', 'month_integer_reference', 'pay_cycle')
                        elif len(creds[1]) == 4 and creds[1].isdigit():
                            payslips = Payslip.objects.filter(year__gte=int(creds[1]))
                elif "BETWEEN" in creds:
                    if len(creds) == 5:
                        if creds[1].isdigit() and creds[2].isdigit() and creds[3].isdigit() and creds[4].isdigit():
                            if len(creds[1]) == 2 and len(creds[3]) == 2:
                                if len(creds[2]) == 4 and len(creds[4]) == 4:
                                    payslips = Payslip.objects.filter(month_integer_reference__range=(int(creds[1]), int(creds[3])), year__range=(int(creds[2]), int(creds[4]))).order_by('-year', 'month_integer_reference', 'pay_cycle')
                    elif len(creds) == 3:
                        if len(creds[1]) == 4 and len(creds[2]) == 4 and creds[1].isdigit() and creds[2].isdigit():
                            payslips = Payslip.objects.filter(year__range=(int(creds[1]), int(creds[2])))
            else:
                employee = Employee.objects.filter(id_number=creds)
                if employee:
                    payslips = Payslip.objects.filter(id_number=employee[0])

            if sorting == "new":
                payslips = payslips.order_by('-year', '-month_integer_reference', '-pay_cycle')
            elif sorting == "old":
                payslips = payslips.order_by('year', 'month_integer_reference', 'pay_cycle')
            elif sorting == "recent":
                payslips = payslips.order_by('-pk')
            
            return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months, 'history':history, 'account':account})
        
        elif button == "create":

            months_as_integers = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
            id_number = request.POST.get("employee")
            month = request.POST.get("month")
            year = int(request.POST.get("year"))
            cycle = int(request.POST.get("cycle"))
            month_integer_reference = months_as_integers[month]

            if id_number == "all":
                employee_list = Employee.objects.all()
            else:
                employee_list = [Employee.objects.get(id_number=id_number)]

            for e in employee_list:
                employee = e
                if Payslip.objects.filter(id_number=employee, month=month, year=year, pay_cycle=cycle).exists() and len(employee_list) == 1:
                    return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months, 'message':'Payslip already exists!', 'history':history, 'account':account})
                elif Payslip.objects.filter(id_number=employee, month=month, year=year, pay_cycle=cycle).exists() and len(employee_list) > 1:
                    pass
                else:
                    rate = employee.getRate()
                    overtime = employee.getOvertime()
                    allowance = employee.getAllowance()
                    if cycle == 2:
                        date_range = '16-31' if month in ['January', 'March', 'May', 'July','August', 'October', 'December'] else '16-29' if (month == 'February' and (year%4==0 and (year%400==0 or year%100!=0))) else '16-28' if month=='February' else '16-30'
                        philhealth = employee.getRate() * 0.04
                        sss = employee.getRate() * 0.045
                        deductions_tax = ((rate/2) + allowance + overtime - philhealth - sss) * 0.2
                        total_pay = ((rate/2) + allowance + overtime - philhealth - sss) - deductions_tax

                        Payslip.objects.create(id_number=employee, employee_name = employee.getName(), month=month, date_range=date_range, year=year, pay_cycle=cycle, rate=rate, earnings_allowance=allowance, deductions_tax=deductions_tax, deductions_health=philhealth, pag_ibig=0, sss=sss, overtime=overtime, total_pay=total_pay, month_integer_reference=month_integer_reference)
                
                    elif cycle == 1:
                        date_range = '1-15'
                        pag_ibig = 100
                        deductions_tax = ((rate/2) + allowance + overtime - pag_ibig) * 0.2
                        total_pay = ((rate/2) + allowance + overtime - pag_ibig) - deductions_tax

                        Payslip.objects.create(id_number=employee, employee_name = employee.getName(), month=month, date_range=date_range, year=year, pay_cycle=cycle, rate=rate, earnings_allowance=allowance, deductions_tax=deductions_tax, deductions_health=0, pag_ibig=pag_ibig, sss=0, overtime=overtime, total_pay=total_pay, month_integer_reference=month_integer_reference)
                    
                    history.append("Created payslip for {} for {} {}, {}, Cycle {}".format(employee.getName(), month, date_range, year, cycle))
                    if len(history) > 5:
                        history.pop(0)
                    Employee.objects.filter(id_number=employee.getID()).update(overtime_pay=0)

            employees = Employee.objects.all()
            return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months, 'message':'Payslip successfully created!', 'history':history, 'account':account})
    else:
        return render(request, 'payroll_app/payslips_page.html', {'payslips':payslips, 'employees':employees, 'months':months, 'history':history})

def create_employee(request):
    global history
    global account
    if (request.method=="POST"):
        button = request.POST.get("button")
        name = request.POST.get("name")
        rate = float(request.POST.get("rate"))
        id_number = int(request.POST.get("id_number"))
        allowance = request.POST.get("allowance")

        if button == "submit":
            if Employee.objects.filter(id_number=id_number).exists():
                return render(request, 'payroll_app/create_employee.html', {'message':'ID already taken!', 'history':history, 'account':account})
            else:
                if not allowance:
                    Employee.objects.create(name=name, rate=rate, id_number=id_number, allowance=0, overtime_pay=0)
                else:
                    Employee.objects.create(name=name, rate=rate, id_number=id_number, allowance=allowance, overtime_pay=0)
                request.session['message'] = "Employee created!"
                return redirect('employees')

    return render(request, 'payroll_app/create_employee.html', {'history':history, 'account':account})

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    request.session['message'] = "Employee deleted."
    return redirect('employees')

def update_employee(request, pk):
    global history
    global account
    if (request.method=="POST"):
        button = request.POST.get("button")
        name = request.POST.get("name")
        rate = float(request.POST.get("rate"))
        allowance = request.POST.get("allowance")
        if allowance == "":
            allowance = 0

        if button == "submit":
            Employee.objects.filter(pk=pk).update(name=name, rate=rate, allowance=allowance)
            request.session['message'] = "Employee details updated!"
            return redirect('employees')
    else:
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html', {'employee':employee, 'history':history, 'account':account})

def view_payslip(request, pk):
    global history
    global account
    payslip = get_object_or_404(Payslip, pk=pk)
    base = payslip.id_number.getRate() / 2
    gross_pay = base + payslip.id_number.getAllowance() + payslip.getOvertime()
    total_deductions = payslip.getDeductions_tax() + payslip.getDeductions_health() + payslip.getSSS() + payslip.getPag_ibig()
    return render(request, 'payroll_app/view_payslip.html', {'payslip':payslip, 'base':base, 'gross':gross_pay, 'deduction':total_deductions, 'history':history, 'account':account})