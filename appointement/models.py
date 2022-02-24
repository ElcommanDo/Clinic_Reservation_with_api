from django.db import models
from accounts.models import Client
# Create your models here.


class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    status = models.CharField(max_length=120, default='pending')
    rescheduled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    mark_as_missed = models.BooleanField(default=False)
    mark_as_finished = models.BooleanField(default=False)

    def __str__(self):
        return '{} appointment'.format(self.client.user.username)

    class Meta:
        ordering = ('-created_at',)


class Reschedule(models.Model):
    app = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reschedule')
    new_date = models.DateTimeField()
    accepted = models.BooleanField(null=True, blank=True)
    waited = models.BooleanField(default=True)


class Notification(models.Model):
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)
