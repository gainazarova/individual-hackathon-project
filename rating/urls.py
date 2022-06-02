from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.RatingCreateApiView.as_view()),
]
