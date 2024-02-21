from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from organization.models import Organization, Product

# Create your models here.


class CustomUser(AbstractUser):
    userId = models.UUIDField(
        primary_key=True, default=uuid.uuid4)
    phone = models.BigIntegerField(null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='organization_user', default="b2df70bc-6f35-4cee-a8bc-e0710116593c")
    is_subscriber = models.BooleanField(default=False)
    is_active_subscriber = models.BooleanField(default=False)
    email_validation = models.BooleanField(default=False)
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_by = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.username


class Contact(models.Model):
    contactId = models.UUIDField(
        primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(
        max_length=100)
    last_name = models.CharField(
        max_length=100)
    email = models.EmailField()
    phone = models.BigIntegerField(null=True)
    company = models.CharField(
        max_length=100)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_contact', default="ed6fc2fb-c616-4bea-b06d-46fc8c46ce8c")
    message = models.CharField(max_length=1000)
    monthly_subscription = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name + self.last_name
