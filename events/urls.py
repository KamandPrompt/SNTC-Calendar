from . import views
from django.urls import path
from allauth.account.views import LogoutView

urlpatterns = [
    path('', views.change_list, name='change_list'),
    path('event/new/', views.event_new, name='event_new'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/delete/',views.event_delete, name='event_delete')
]
