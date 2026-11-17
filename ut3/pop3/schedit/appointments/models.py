from django.conf import settings
from django.db import models
from django.urls import reverse


class Appointment(models.Model):
    date = models.DateField()
    slot = models.ForeignKey('slots.Slot', related_name='appointments', on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='appointments', on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('date', 'slot')
        ordering = ['date', 'slot']

    def __str__(self):
        return f'{self.date} ({self.slot})'

    def get_absolute_url(self):
        return reverse('appointments:appointments-detail', kwargs={'pk': self.pk})
