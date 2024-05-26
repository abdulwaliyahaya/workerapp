"""workerapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter
from visit_analytics.views import get_units, make_visit
from visit_analytics.converter import FloatConverter

register_converter(FloatConverter, 'float')
urlpatterns = [
    path('units', get_units, name='list_of_units'),
    path('make-visit/<int:pk>/<float:longitude>/<float:latitude>/', make_visit, name='make_visit')
]
