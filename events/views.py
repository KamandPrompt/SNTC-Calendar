# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from.models import Event
from django.shortcuts import render
from datetime import datetime
def change_list(request):
    curr_time=datetime.now().time()
    curr_date=datetime.now().date()
    evs=Event.objects.filter(day__gte=curr_date).order_by('end_time')
    return render(request, 'events/change_list.html', {'events':evs,'time':curr_time,'date':curr_date})
# Create your views here.
