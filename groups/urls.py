from django.urls import path
from . import views

urlpatterns = [
    path('', views.chama_list, name='chama_list'),
    path('members/', views.member_list, name='member_list'),
    path('contributions/', views.contribution_list, name='contribution_list'),
    path('loans/', views.loan_list, name='loan_list'),
    path('chamas/add/', views.add_chama, name='add_chama'),
]  