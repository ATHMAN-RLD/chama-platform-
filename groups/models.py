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


class Member(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Membership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Ordinary Member'),
        ('treasurer', 'Treasurer'),
        ('chairperson', 'Chairperson'),
    ]

    chama = models.ForeignKey(Chama, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('chama', 'member')

    def __str__(self):
        return f"{self.member.full_name} in {self.chama.name}"   