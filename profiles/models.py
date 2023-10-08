from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserDetail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    telephone = models.CharField(max_length=50, null=True)
    address1 = models.CharField(max_length=100, null=True)
    address2 = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    county = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"User: {self.user_id} || Telephone: {self.telephone} || Address1: {self.address1} || PostalCode: {self.postal_code} || City: {self.city} || County: {self.county}"