from django.urls import path, include, re_path
from . import views

app_name = 'Accounts'

urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('home_api/', views.home_api, name = 'home_api'),
    path('campaign/', views.campaign, name = 'campaign'),
    path('how-to/', views.how_to, name = 'how-to'),
]

