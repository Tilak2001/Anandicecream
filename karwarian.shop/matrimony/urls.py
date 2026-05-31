from django.urls import path
from . import views

app_name = 'matrimony'

urlpatterns = [
    path('', views.matrimony_list, name='list'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('profile/<int:pk>/', views.profile_detail, name='detail'),
]
