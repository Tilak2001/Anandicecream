from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.second_hand_list, name='goods_hub'),
    path('second-hand/', views.second_hand_list, name='second_hand_list'),
    path('second-hand/add/', views.second_hand_add, name='second_hand_add'),
    path('category/<slug:category_slug>/', views.second_hand_list, name='second_hand_category'),
    path('browse/', views.services_list, name='list'),
    path('add/', views.services_add, name='add'),
    path('function-services/', views.function_services_hub, name='function_hub'),
    path('function-services/<str:segment>/', views.function_services_section, name='function_section'),
    path(
        'function-services/<str:segment>/<slug:subcategory>/',
        views.function_services_listings,
        name='function_listings',
    ),
    path('<slug:slug>/', views.service_detail, name='detail'),
]
