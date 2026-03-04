
from django.contrib import admin
from django.urls import path

from hospitalapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name = 'home'),

    path('starter/', views.starter, name = 'starter'),

    path('about/', views.about, name = 'about'),

    path('appointment/', views.appointment, name = 'appointment'),

    path('services/', views.services, name = 'services'),

    path('departments/', views.departments, name = 'departments'),

    path('doctors/', views.doctors, name = 'doctors'),

    path('contact/', views.contact, name = 'contact'),
]

