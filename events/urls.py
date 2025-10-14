from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),
    path('event/<slug:slug>/add-car/', views.add_car, name='add_car'),
    path('event/<slug:slug>/add-member/', views.add_member, name='add_member'),
    path('event/<slug:slug>/member/<int:member_id>/update/', views.update_member, name='update_member'),
    path('event/<slug:slug>/member/<int:member_id>/delete/', views.delete_member, name='delete_member'),
    path('event/<slug:slug>/car/<int:car_id>/delete/', views.delete_car, name='delete_car'),
]