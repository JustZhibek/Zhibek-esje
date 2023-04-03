from django.contrib.auth.models import User, AbstractUser
from django.db import models


class ConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    valid_until = models.DateTimeField()

    def __str__(self):
        return self.code
