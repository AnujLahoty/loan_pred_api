from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
    path('api/', views.api_req_pred),
    path('', views.cxcontact, name='cxform'),
 
] 