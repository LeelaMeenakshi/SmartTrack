from django.urls import path
from . import views


urlpatterns = [

path('', views.index_view, name='index'),

path('signup/', views.signup_view, name='signup'),

path('login/', views.login_view, name='login'),

path('dashboard/', views.dashboard_view, name='dashboard'),
path('courses/', views.courses_view, name='courses'),

path('logout/', views.logout_view, name='logout'),
path('basket/', views.basket, name = 'basket'),
path('planner/', views.planner_view, name = 'planner'),
path('reports/', views.reports, name = 'reports'),
path('search-course/', views.search_course, name = 'search_course'),
path('save-semester/', views.save_semester, name = 'save-semester'),
path("get-semesters/", views.get_semesters, name="get_semesters"),
path("remove-course/", views.remove_course, name="remove_course"),
path("basket-analysis/", views.basket_analysis, name="basket_analysis"),
path("history-data/", views.history_data, name="history_data"),
path(
    "planner-search-course/",
    views.planner_search_course,
    name="planner_search_course",
),
path("planner/add-course/", views.add_planned_course, name="add_planned_course"),
path(
    "planner/remove-course/",
    views.remove_planned_course,
    name="remove_planned_course"
),


]