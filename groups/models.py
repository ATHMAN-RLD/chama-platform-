from django.db import models

# Create your models here.
class Chama(models.Model):
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    contribution_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contribution_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='weekly')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name  