from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('clients/', client),
    path('clients/<int:id>', client),
    path('clients/<int:id>/projects/', project),
    path('projects/', project),
]
