from django.urls import path
from .views import home_view, pi_view, demo_json_view

urlpatterns = [
    path('', home_view, name='home'),
    path('pi_view/', pi_view, name='pi_view'),
    path('pi_view/json/', demo_json_view, name='demo_json_view')
]
