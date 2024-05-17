from django.urls import path
from . import views

urlpatterns = [
    path('find_similar_actor/', views.find_similar_actor, name='find_similar_actor'),
]