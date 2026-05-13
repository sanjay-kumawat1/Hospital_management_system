from django.db import models

# Create your models here.
from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    prescription = models.TextField()
    file = models.FileField(upload_to='records/')

    def __str__(self):
        return f"Record of {self.patient}"