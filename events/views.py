# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from.models import Event
from django.shortcuts import render
from datetime import datetime, timedelta

def change_list(request):
    curr_time=datetime.now().time()
    curr_date=datetime.now().date()
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
