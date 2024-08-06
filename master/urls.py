from django.urls import path
from . import views



urlpatterns = [

    #--------------------------- Dashboard URL -----------------------------------------------------------------------

    path('dashboard/', views.dashboard, name='dashboard'),
    
    #-------------------------- URLS OF DEPARTMENT------------------------------------------------------------------

    path('department_list/', views.department_list, name='department_list'),
    path('department_add/', views.department_add, name='department_add'),
    path('department_edit/<int:department_id>/', views.department_edit, name='department_edit'),
    path('department_view/<int:department_id>/', views.department_view, name='department_view'),
    path('department_delete/<int:department_id>/', views.department_delete, name='department_delete'),
    path('download_template/', views.download_template, name='download_template'),
    path('bulk_upload/', views.bulk_upload, name='bulk_upload'),
    path('export_departments/', views.export_departments, name='export_departments'),

    
    #-------------------------- URLS OF DESIGNATION------------------------------------------------------------------

    path('designation_list/', views.designation_list, name='designation_list'),
    path('designation_add/', views.designation_add, name='designation_add'),
    path('designation_edit/<int:designation_id>/', views.designation_edit, name='designation_edit'),
    path('designation_view/<int:designation_id>/', views.designation_view, name='designation_view'),
    path('designation_delete/<int:designation_id>/', views.designation_delete, name='designation_delete'),
    path('designation_download_template/', views.designation_download_template, name='designation_download_template'),
    path('designation_bulk_upload/', views.designation_bulk_upload, name='designation_bulk_upload'),
    path('export_designations/', views.export_designations, name='export_designations'),

    #-------------------------- URLS OF LOCATIONS------------------------------------------------------------------

    path('location_list/', views.location_list, name='location_list'),
    path('location_add/', views.location_add, name='location_add'),
    path('location_edit/<int:location_id>/', views.location_edit, name='location_edit'),
    path('location_view/<int:location_id>/', views.location_view, name='location_view'),
    path('location_delete/<int:location_id>/', views.location_delete, name='location_delete'),
    path('download_location_template/', views.download_location_template, name='download_location_template'),
    path('location_bulk_upload/', views.location_bulk_upload, name='location_bulk_upload'),
    path('export_locations/', views.export_locations, name='export_locations'),

    #-------------------------- URLS OF EMPLOYEE------------------------------------------------------------------

    path('employee_list', views.employee_list, name='employee_list'),
    path('employee_add', views.employee_add, name='employee_add'),
    path('designations_of_department', views.designations_of_department, name='designations_of_department'),
    path('employee_edit/<str:employee_id>/', views.employee_edit, name='employee_edit'),
    
]