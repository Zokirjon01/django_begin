from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('page/<str:page>/', views.main_page, name='main_page'),
]
