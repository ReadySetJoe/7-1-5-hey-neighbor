from django.db import models
from datetime import date
from django.urls import reverse

class Tools(models.Model):
    WEEKS = 'WEEKLS'
    DAYS = 'DAYS'
    HOURS = 'HOURS'

    AVAILABLE_CHOICES = [
        (HOURS, 'Hours'),
        (DAYS, 'Days'),
        (WEEKS, 'Weeks'),
    ]

    name = models.CharField(max_length=255)
    available = models.CharField(max_length=255, choices=AVAILABLE_CHOICES)
    description = models.CharField(max_length=255)
    powered = models.BooleanField(default=False)
    added_date = models.DateField('date added', default=date.today)
    watchers = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tools:index')
