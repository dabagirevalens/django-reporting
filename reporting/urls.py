from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.businesses, name='dashboard')
]

urlpatterns += staticfiles_urlpatterns()