from django.urls import path
from Chat import views

urlpatterns = [
    path('', views.chat, name='chat'),
    path('intent/', views.web_inbound, name='web_inbound')
]