from django.db import models

from account.models import CustomUser
from patients.models import PatientCard


class Action(models.Model):
    author = models.ForeignKey(CustomUser, null=True, related_name="actions", on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=100)
    target = models.ForeignKey(PatientCard, null=True, related_name="actions", on_delete=models.SET_NULL)
    target_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    action_text = models.CharField(max_length=200)
