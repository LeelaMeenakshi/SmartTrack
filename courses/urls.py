from django.urls import path
from . import views


urlpatterns = [

path('', views.index_view, name='index'),

path('signup/', views.signup_view, name='signup'),

path('login/', views.login_view, name='login'),

path('dashboard/', views.dashboard_view, name='dashboard'),
path('courses/', views.courses_view, name='courses'),

path('logout/', views.logout_view, name='logout'),
path('basket/', views.basket_view, name = 'basket'),
path('planner/', views.planner_view, name = 'planner'),
path('reports/', views.reports_view, name = 'reports'),
path('search-course/', views.search_course, name = 'search_course'),
path('save-semester/', views.save_semester, name = 'save-semester'),

]