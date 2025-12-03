from django.db import models

class Emp(models.Model):
    empno=models.IntegerField(primary_key=True)
    First_Name=models.CharField(max_length=30)
    Last_Name=models.CharField(max_length=30)
    Location=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    salary=models.IntegerField(null=True)

    def __str__(self):
        return self.First_Name

