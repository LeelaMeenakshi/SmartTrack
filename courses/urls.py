from django.urls import path
from . import views


urlpatterns = [

path('', views.index_view, name='index'),

path('signup/', views.signup_view, name='signup'),

path('login/', views.login_view, name='login'),

path('dashboard/', views.dashboard_view, name='dashboard'),

path('logout/', views.logout_view, name='logout'),

]