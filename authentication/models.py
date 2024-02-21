from django.db import models

# Create your models here.


class OTP(models.Model):
    otp_key = models.CharField(primary_key=True, max_length=100)
    created = models.DateTimeField(
        editable=False, auto_now_add=True)
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.otp_key
