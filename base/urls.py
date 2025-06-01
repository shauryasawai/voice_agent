from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-voice/', views.process_voice, name='process_voice'),
]