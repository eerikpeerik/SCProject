from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', views.list_view, name='list'),  # Root page for the app
    path('add/', views.add_item, name='add_item'),
    path('<int:item_id>/delete/', views.delete_item, name='delete_item'),
]

