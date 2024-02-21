from django.db import models
import uuid
from organization.models import Organization

# Create your models here.


class Subscription(models.Model):
    subscription_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    subscription_name = models.CharField(max_length=50)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='organization_subscription', default="b2df70bc-6f35-4cee-a8bc-e0710116593c")
    start_date = models.DateField()
    end_date = models.DateField()
    updated_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_by = models.CharField(max_length=50, editable=False)

    def __str__(self):
        return self.subscription_name
