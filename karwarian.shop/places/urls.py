from django.urls import path
from . import views

app_name = 'places'

urlpatterns = [
    path('', views.places_list, name='list'),
    path('category/<slug:slug>/', views.places_by_category, name='by_category'),
    path('<slug:slug>/', views.place_detail, name='detail'),
]
