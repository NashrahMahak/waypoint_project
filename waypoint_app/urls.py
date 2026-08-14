from django.contrib import admin
from django.urls import path
from waypoint_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('trail/<str:trail_id>/', views.trail_detail, name='trail_detail'),
    path('report/', views.report, name='report'),
    path('search/', views.search, name='search'),
]