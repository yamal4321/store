from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

class Seller(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  date_created = models.DateTimeField(default=timezone.now)

class Product(models.Model):
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=100)
  description = models.CharField(max_length=100, null=True)
  price = models.IntegerField()
  details = models.TextField(null=True)
  delivery = models.TextField(null=True)
  contacts = models.TextField(null=True)
  photo = models.CharField(max_length=100, default="default.jpg")
  user_uuid = models.ForeignKey(Seller, to_field='uuid', on_delete=models.CASCADE)  
  votes = models.IntegerField(null=False, default=0)  
  category = models.CharField(max_length=100, default="null")
