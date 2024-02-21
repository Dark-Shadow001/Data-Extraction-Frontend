from django.db import models
import uuid

# Create your models here.


class Organization(models.Model):
    class Meta:
        unique_together = (('organization_id', 'organization_name'),)

    organization_id = models.CharField(primary_key=True,
                                       max_length=50, default=uuid.uuid4)
    organization_name = models.CharField(max_length=50, unique=True)
    website = models.CharField(max_length=100)
    contact_email = models.EmailField()
    country = models.CharField(max_length=75)
    organization_image_link = models.CharField(max_length=200)
    organization_image_link_dark = models.CharField(max_length=200, null=True)
    subscription_start_date = models.DateField(null=True)
    subscription_end_date = models.DateField(null=True)
    is_subscrition_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_by = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.organization_name


class Product(models.Model):
    product_id = models.CharField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=50)
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=250)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_by = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.product_name
