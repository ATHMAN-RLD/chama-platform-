from django.urls import path
from . import views

urlpatterns = [
    path('', views.chama_list, name='chama_list'),
    path('members/', views.member_list, name='member_list'),
]   