# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
from datetime import datetime
# Create your models here.
def_end=datetime.now().replace(hour=23,minute=59)
def_start=datetime.now().replace(hour=0,minute=0)
class Event(models.Model):
    club = models.CharField(u'Club name', max_length=100, blank=False, null=True)
    created_by_email = models.CharField(u'Email of Creator', max_length=100, blank=True, null=False)

    # Maps to summary
    name = models.CharField(u'Event Details', max_length=200, null=True, blank=False)

    # Maps to start_date_time and end_date_time
    day = models.DateField(u'Day of the event')
    start_time = models.TimeField(u'Starting time')
    end_time = models.TimeField(u'Final time')

    # Maps to location
    venue = models.CharField(u'Venue or location',max_length=100, blank=True, null=True, default='TBA')

    # Maps to description of the event
    description = models.TextField(u'Description of the Event', null=True, blank=True)

    # A check if overlap should be allowed
    overlap = models.BooleanField(u'Allow overlaps',default=False,blank=False,null=False)

    # Maps to google calender event
    id = models.CharField(u'Event Id', max_length=200, primary_key=True)
    event_link = models.CharField(u'Google Calender Event Link', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = u'Scheduling'
        verbose_name_plural = u'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Ending hour must be after the starting hour')

        events = Event.objects.filter(day=self.day).exclude(id=self.id)
        if events.exists():
            for event in events:
                if not event.overlap and self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

class Subscription(models.Model):
    # Stores the information for each club
    id = models.AutoField(primary_key=True)
    club_email = models.CharField(u'Club Email', max_length=100, blank=False, null=False)
    student_email = models.CharField(u'Student Email', max_length=100)
