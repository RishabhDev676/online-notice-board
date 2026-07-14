from django.urls import path
from . import views

urlpatterns = [

    # Home page (all notices)
    path('', views.home, name='home'),

    # Categories
    path('categories/', views.categories, name='categories'),
    path('category/<slug:slug>/', views.category_notices, name='category_notices'),

    # Departments
    path('departments/', views.departments, name='departments'),
    path('department/<slug:slug>/', views.department_notices, name='department_notices'),
]
