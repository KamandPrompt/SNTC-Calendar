# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from events.calender_utils import CalenderEventsUtil
from.models import Event, Subscription
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
import pytz
from .forms import EventForm
from allauth.socialaccount.models import SocialToken

def change_list(request):
    utc_time = datetime.utcnow()
    gmt_timezone = pytz.timezone("GMT")
    timezone = pytz.timezone("Asia/Kolkata")
    utc_time = gmt_timezone.localize(utc_time)
    curr_time=utc_time.astimezone(timezone).time()
    curr_date=utc_time.astimezone(timezone).date()
    evs=Event.objects.filter(day__gte=curr_date)
    evs=sorted(evs,key=lambda x: (x.day,x.start_time))
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
            d["event_link"]=e.event_link
            b=False
            if i==0:
                b=True
            elif prev!=e.day :
                b=True
                if prev > nextday:
                    b=False
            d["change"]=b
            d["pk"] = e.pk
            evs_with_changes.append(d)
            prev=d["day"]
            i+=1
    try:
        usr = request.user.first_name + " " + request.user.last_name
    except:
        usr = request.user
    return render(request, 'events/change_list.html', {
        'events': evs_with_changes,
        'time': curr_time,
        'date': curr_date,
        'tomorrow': nextday,
        'user':usr })

def has_calender_access(user):
    result = SocialToken.objects.filter(account__user=user, account__provider='google')

    if len(result) == 0:
        return False, None, None

    result = result.get()
    refresh_token = result.__dict__.get('token_secret')
    access_token = result.__dict__.get('token')
    expires_at = result.__dict__.get('expires_at')

    if refresh_token is None:
        # Check if access token is valid or not
        if access_token is None:
            return False, None, None
        else:
            now = datetime.now()
            if now + timedelta(minutes=30) > expires_at:
                print("Access token expired!")
                return False, access_token, None
    
    return True, access_token, refresh_token

def handle_calender_event(user, event, access_token, refresh_token, method='create'):
    ''' Creates the calender event and returns the values
        @params method : 'create', 'update'
    '''

    google_calender = CalenderEventsUtil(
        access_token=access_token,
        refresh_token=refresh_token
    )

    calender_response = None
    if method == 'delete':
        calender_response = google_calender.delete_calender_event(event.id)
    else:
        event.club = user.first_name + " " + user.last_name
        event.created_by_email = user.email

        start_date_time = event.day.isoformat() + "T" + event.start_time.isoformat()
        end_date_time = event.day.isoformat() + "T" + event.end_time.isoformat()

        subscriptions = Subscription.objects.filter(club_email=user.email)
        attendees_emails = list(subscriptions.values_list('student_email', flat=True))

        # Now use the above google_calender object to create a new event
        # TODO - Allow invites to be added
        event_data = google_calender.create_event_data(
            str(event.name),
            str(event.venue) + ', IIT Mandi',
            str(event.description),
            start_date_time,
            end_date_time,
            attendees_emails,
        )

        if method == 'update':
            calender_response = google_calender.update_calender_event(event.id, event_data)
        else:
            calender_response = google_calender.create_calender_event(event_data)

    if calender_response.get('success'):
        event.id = calender_response.get('event_id')
        event.event_link = calender_response.get('event_link')

        if method == 'delete':
            event.delete()
        else:
            event.save()

        return redirect('change_list')                
    else:
        resp = "Event " + str(method) + " failed on Google Calender" + str(calender_response)
        print(resp)
        return JsonResponse({"error": resp})

def event_new(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login')

    has_access, access_token, refresh_token = has_calender_access(request.user)
    if not has_access:
        return redirect('/accounts/google/login')

    # We have refresh token, so we are good to go to create calender event
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            return handle_calender_event(request.user, event, access_token, refresh_token, method='create')
    else:
        form = EventForm()
    return render(request, 'events/event_edit.html', {'form': form})

def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.is_authenticated  or request.user.first_name not in event.club:
        return redirect('/accounts/google/login')

    has_access, access_token, refresh_token = has_calender_access(request.user)
    if not has_access:
        return redirect('/accounts/google/login')

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            return handle_calender_event(request.user, event, access_token, refresh_token, method='update')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if not request.user.is_authenticated  or request.user.first_name not in event.club:
        return redirect('/accounts/google/login')

    has_access, access_token, refresh_token = has_calender_access(request.user)
    if not has_access:
        return redirect('/accounts/google/login')

    event = Event.objects.filter(pk=pk)
    event.id = pk
    return handle_calender_event(request.user, event, access_token, refresh_token, method='delete')

def subscription_list(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login')

    return JsonResponse({"hello": "world"})
