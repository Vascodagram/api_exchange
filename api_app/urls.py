from django.urls import path
from .views import TestView


urlpatterns = [
    path('price/', TestView.as_view()),
]
