from django.conf.urls import url,include
from . import views
from django.urls import path

urlpatterns = [
    path('', views.change_list, name='change_list'),
    path('event/new/', views.event_new, name='event_new'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
]
