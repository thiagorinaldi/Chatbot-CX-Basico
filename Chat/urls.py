from django.urls import path
from Chat import views

urlpatterns = [
    path('', views.web_inbound, name='web_inbound')
]