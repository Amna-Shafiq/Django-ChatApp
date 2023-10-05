from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('start-chat/<int:connection_id>/', views.start_chat, name='start_chat'),
    path('start-chat/', views.start_chat, name='initial_start_chat'),
    # path('', views.home_page, name='home-page'),
    path('', views.start_chat, name='initial_start_chat'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('all_users', views.users, name='users'),
    path('user_settings', views.user_settings, name='user_settings'),

]
