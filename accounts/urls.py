from django.urls import path
from . import views
from django.shortcuts import redirect

urlpatterns = [

    path('', lambda request: redirect('admin_login')),

    path('login/', views.admin_login, name='admin_login'),
    path('register/', views.admin_register, name='admin_register'),

    path('pending-admins/', views.pending_admins, name='admin_pending_admins'),
    path('approve-admin/<int:pk>/', views.approve_admin, name='admin_approve_admin'),
    path('admins/', views.admin_list, name='admin_admin_list'),
    path('remove-admin/<int:pk>/', views.remove_admin, name='admin_remove_admin'),

    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='admin_dashboard'),

    ## Management
    # Notice 
    path('notices/', views.notice_list, name='admin_notice_list'),
    path('notices/add/', views.notice_add, name='admin_notice_add'),
    path('notices/edit/<int:pk>/', views.notice_edit, name='admin_notice_edit'),
    path('notices/delete/<int:pk>/', views.notice_delete, name='admin_notice_delete'),

    # Categories
    path('categories/', views.category_list, name='admin_category_list'),
    path('categories/add/', views.category_add, name='admin_category_add'),
    path('categories/delete/<int:pk>/', views.category_delete, name='admin_category_delete'),
    path('categories/edit/<int:pk>/', views.category_edit, name='admin_category_edit'),

    # Departments
    path('departments/', views.department_list, name='admin_department_list'),
    path('departments/add/', views.department_add, name='admin_department_add'),
    path('departments/delete/<int:pk>/', views.department_delete, name='admin_department_delete'),
    path('departments/edit/<int:pk>/', views.department_edit, name='admin_department_edit'),

    # Subscription
    path('subscriptions/', views.subscription_list, name='admin_subscription_list'),
    path('subscriptions/delete/<int:pk>/', views.subscription_delete, name='admin_subscription_delete'),

]
