from django.urls import path
from . import views
from . import dashboard_views
from . import auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('bus-timings/', views.bus_timings, name='bus_timings'),
    path('cricket-score/', views.cricket_score, name='cricket_score'),
    
    # User authentication (matrimony & members)
    path('accounts/login/', auth_views.user_login, name='user_login'),
    path('accounts/register/', auth_views.user_register, name='user_register'),
    path('accounts/logout/', auth_views.user_logout, name='user_logout'),

    # Matrimony
    path('matrimony/', views.matrimony_list, name='matrimony_list'),
    path('matrimony/profile/<int:profile_id>/', views.matrimony_detail, name='matrimony_detail'),
    path('matrimony/add/', views.matrimony_add, name='matrimony_add'),
    
    # Dashboard
    path('dashboard/login/', dashboard_views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', dashboard_views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/', dashboard_views.dashboard_home, name='dashboard_home'),
    
    # Dashboard - Cricket
    path('dashboard/cricket/', dashboard_views.cricket_list, name='cricket_list'),
    path('dashboard/cricket/add/', dashboard_views.cricket_add, name='cricket_add'),
    path('dashboard/cricket/<int:match_id>/edit/', dashboard_views.cricket_edit, name='cricket_edit'),
    path('dashboard/cricket/<int:match_id>/live/', dashboard_views.cricket_live_update, name='cricket_live_update'),
    path('dashboard/cricket/<int:match_id>/delete/', dashboard_views.cricket_delete, name='cricket_delete'),
    
    # Dashboard - Orders
    path('dashboard/orders/', dashboard_views.orders_list, name='dashboard_orders'),
    path('dashboard/orders/<str:order_id>/update/', dashboard_views.order_update_status, name='dashboard_order_update'),
    
    # Dashboard - News
    path('dashboard/news/', dashboard_views.news_list, name='dashboard_news'),
    path('dashboard/news/add/', dashboard_views.news_add, name='dashboard_news_add'),
    path('dashboard/news/<int:news_id>/delete/', dashboard_views.news_delete, name='dashboard_news_delete'),
    
    # Dashboard - Services Moderation
    path('dashboard/services/', dashboard_views.dashboard_services, name='dashboard_services'),
    path('dashboard/services/<int:service_id>/update-status/', dashboard_views.dashboard_services_update_status, name='dashboard_services_update_status'),
    path('dashboard/services/<int:service_id>/delete/', dashboard_views.dashboard_services_delete, name='dashboard_services_delete'),
    
    # Dashboard - Matrimony
    path('dashboard/matrimony/', dashboard_views.matrimony_dashboard_list, name='matrimony_dashboard_list'),
    path('dashboard/matrimony/add/', dashboard_views.matrimony_dashboard_add, name='matrimony_dashboard_add'),
    path('dashboard/matrimony/<int:profile_id>/update-status/', dashboard_views.matrimony_dashboard_update_status, name='matrimony_dashboard_update_status'),
    path('dashboard/matrimony/<int:profile_id>/delete/', dashboard_views.matrimony_dashboard_delete, name='matrimony_dashboard_delete'),
    
    # Public API
    path('api/cricket/matches/', dashboard_views.cricket_api_matches, name='cricket_api_matches'),
]
