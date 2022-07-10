from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_unlog, name='index_unlog'),
    path('login', views.login, name='login'),
]
