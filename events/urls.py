from django.conf.urls import url,include
from . import views
urlpatterns = [
    url('', views.change_list, name='change_list'),
]