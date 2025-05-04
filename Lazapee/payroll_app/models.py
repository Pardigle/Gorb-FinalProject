from django.db import models

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

class Employee(models.Model):
    name = models.CharField(max_length = 300)
    id_number = models.CharField(max_length = 300, unique = True)
    rate = models.FloatField()
    overtime_pay = models.FloatField(null=True)
    allowance = models.FloatField(null=True)

    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number
    
    def getRate(self):
        return self.rate
    
    def getOvertime(self):
        return self.overtime_pay
    
    def resetOvertime(self):
        self.overtime_pay = 0

    def getAllowance(self):
        return self.allowance
    
    def __str__(self):
        return "pk: {}, rate: {}".format(self.id_number, self.rate)
    
class Payslip(models.Model):
    id_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length = 300) ##ADDITIONAL FIELD (Why? So the name of employee at the time of generation is hard-coded in each payslip.)
    month = models.CharField(max_length = 300)
    month_integer_reference = models.IntegerField() ##ADDITIONAL FIELD (Why? So we are able to sort the payslips in manner of time. E.g. Jan = 1, Feb = 2, ...)
    date_range = models.CharField(max_length = 300)
    year = models.CharField(max_length = 300)
    pay_cycle = models.IntegerField()
    rate = models.FloatField()
    earnings_allowance = models.FloatField()
    deductions_tax = models.FloatField()
    deductions_health = models.FloatField()
    pag_ibig = models.FloatField()
    sss = models.FloatField()
    overtime = models.FloatField()
    total_pay = models.FloatField()

    def getIDNumber(self):
        return self.id_number.getID()
    
    def getMonth(self):
        return self.month
    
    def getDate_range(self):
        return self.date_range
    
    def getYear(self):
        return self.year
    
    def getPay_cycle(self):
        return self.pay_cycle
    
    def getRate(self):
        return self.rate
    
    def getCycleRate(self):
        return self.rate / 2
    
    def getEarnings_allowance(self):
        return self.earnings_allowance
    
    def getDeductions_tax(self):
        return self.deductions_tax
    
    def getDeductions_health(self):
        return self.deductions_health
    
    def getPag_ibig(self):
        return self.pag_ibig
    
    def getSSS(self):
        return self.sss
    
    def getOvertime(self):
        return self.overtime
    
    def getTotal_pay(self):
        return self.total_pay
    
    def __str__(self):
        return "pk: {}, Employee: {}, Period: {} {}, {}, Cycle: {}, Total Pay: {}".format(self.pk, self.id_number, self.month, self.date_range, self.year, self.pay_cycle, self.total_pay)