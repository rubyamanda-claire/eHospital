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
    name = models.CharField()
    email = models.EmailField()
    areaofspecialization = models.CharField()
    phonenumber = models.IntegerField() 

    def __str__(self):
        return self.name 

