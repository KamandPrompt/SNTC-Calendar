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
    club= models.CharField(u'Club name', max_length=100, blank=False, null=True)
    name = models.TextField(u'Event Details', null=True,blank=False)
    day = models.DateField(u'Day of the event')
    start_time = models.TimeField(u'Starting time')
    end_time = models.TimeField(u'Final time')
    venue= models.CharField(u'Venue or link',max_length=100, blank=True, null=True, default='TBA')
    overlap = models.BooleanField(u'Allow overlaps',default=False,blank=False,null=False)

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
