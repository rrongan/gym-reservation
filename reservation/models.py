from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    USERTYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Default', 'Default'),
    )
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)
    user_type = models.CharField(max_length=15, choices=USERTYPE_CHOICES, default='Default')

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return "%s (%s)" % (self.get_full_name(), self.username)

    def __unicode__(self):
        return u"%s (%s)" % (self.get_full_name(), self.username)


class Facility(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Declined', 'Declined'),
        ('Approved', 'Approved'),
    )
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fid = models.ForeignKey(Facility, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    time = models.TimeField(default=datetime.now() + timedelta(seconds=60), blank=True)
    duration = models.FloatField(default=0, validators=[MinValueValidator(0.5)])
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')

    def get_start_time(self):
        return datetime.combine(self.date, self.time).time()

    def get_end_time(self):
        dt = datetime.combine(self.date, self.time) + timedelta(minutes=self.duration*60)
        return dt.time()

    def get_start_datetime(self):
        return datetime.combine(self.date, self.time)

    def get_end_datetime(self):
        return datetime.combine(self.date, self.time) + timedelta(minutes=self.duration*60)
