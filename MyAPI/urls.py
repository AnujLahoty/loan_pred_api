from django.urls import path, include
from . import views
from rest_framework import routers


urlpatterns = [
	# path('form/', views.myform, name='myform'),
    path('api/', views.api_req_pred),
    path('form/', views.cxcontact, name='cxform'),
 
] 