from django.conf.urls import url
from . import views
from django.urls import re_path, path

app_name = 'public'

urlpatterns = [
    path('', views.terms, name='terms')

]
