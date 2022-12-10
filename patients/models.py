from django.db import models

from account.models import CustomUser


class PatientCard(models.Model):
    full_name = models.CharField(max_length=100)
    home_address = models.CharField(max_length=500)
    date_of_birth = models.DateField()


class ExaminationNote(models.Model):
    card = models.ForeignKey(PatientCard,
                             related_name="examination_notes",
                             on_delete=models.CASCADE)
    doctor = models.ForeignKey(CustomUser,
                               related_name="examination_notes",
                               on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()





