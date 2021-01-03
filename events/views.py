# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from.models import Event
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import pytz
from .forms import EventForm

def change_list(request):
    utc_time = datetime.utcnow()
    gmt_timezone = pytz.timezone("GMT")
    timezone = pytz.timezone("Asia/Kolkata")
    utc_time = gmt_timezone.localize(utc_time)
    curr_time=utc_time.astimezone(timezone).time()
    curr_date=utc_time.astimezone(timezone).date()
    evs=Event.objects.filter(day__gte=curr_date)
    evs=sorted(evs,key=lambda x: (x.day,x.end_time))
    evs_with_changes=[]
    i=0
    prev=0
    nextday= datetime.today() + timedelta(days=1)
    nextday=nextday.date()
    for e in evs:
        if (e.day > curr_date or e.end_time > curr_time):
            d={}
            d["club"]=e.club
            d["end_time"]=e.end_time
            d["start_time"]=e.start_time
            d["day"]=e.day
            d["name"]=e.name
            d["venue"]=e.venue
            b=False
            if i==0:
                b=True
            elif prev!=e.day :
                b=True
                if prev > nextday:
                    b=False
            d["change"]=b
            evs_with_changes.append(d)
            prev=d["day"]
            i+=1
    return render(request, 'events/change_list.html', {'events':evs_with_changes,'time':curr_time,'date':curr_date,'tomorrow':nextday})
# Create your views here.

def event_new(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login')
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = str(request.user).upper()
            event.save()
            return redirect('change_list')
    else:
        form = EventForm()
    return render(request, 'events/event_edit.html', {'form': form})
