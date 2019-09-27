# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def change_list(request):
    return render(request, 'events/change_list.html', {})
# Create your views here.
