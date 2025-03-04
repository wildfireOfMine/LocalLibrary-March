from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from api import views

app_name = 'api'
urlpatterns = [
    path('autor/', views.autor_api_view, name='autor-api'),
    path('autor/<int:pk>', views.autor_detail_view, name='autor_detail_view'),
]
