from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.CharField(max_length = 20)
    email = models.EmailField()
    gender = models.CharField(max_length = 10)
    age = models.IntegerField()
    dob = models.DateField()
    admission = models.DateTimeField()
    medicalhistory = models.TextField()

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    areaofspecialization = models.CharField(max_length=100)
    phonenumber = models.IntegerField() 

    def __str__(self):
        return self.name 
    
class MyAppointment(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    datetime = models.DateTimeField()
    department = models.CharField(max_length=20)
    doctor = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.status}"

