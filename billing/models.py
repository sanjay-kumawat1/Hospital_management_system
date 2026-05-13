from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Invoice(models.Model):

    STATUS_CHOICES = [
        ('pending', '⏳ Pending'),
        ('paid', '✅ Paid'),
        ('overdue', '⚠️ Overdue'),
        ('cancelled', '❌ Cancelled'),
    ]

    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=15, blank=True)
    appointment_details = models.CharField(max_length=300)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.id} - {self.patient_name} - ₹{self.amount}"

    def save(self, *args, **kwargs):
        if self.due_date and self.status == 'pending':
            if self.due_date < timezone.now().date():
                self.status = 'overdue'
        super().save(*args, **kwargs)

    def mark_paid(self):
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()