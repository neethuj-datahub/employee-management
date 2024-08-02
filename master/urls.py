from django.urls import path
from . import views



urlpatterns = [

    path('dashboard/', views.dashboard, name='dashboard'),
    #-------------------------- URLS OF DEPARTMENT------------------------------------------------------------------

    path('departments/', views.department_list, name='department_list'),
    path('department_add/', views.department_add, name='department_add'),
    path('department_edit/<int:department_id>/', views.department_edit, name='department_edit'),
    path('department_view/<int:department_id>/', views.department_view, name='department_view'),
    path('department_delete/<int:department_id>/', views.department_delete, name='department_delete'),
    path('download_template/', views.download_template, name='download_template'),
    path('bulk_upload/', views.bulk_upload, name='bulk_upload'),
    path('export_departments/', views.export_departments, name='export_departments'),

    #-------------------------- END OF URLS OF DEPARTMENT------------------------------------------------------------------
    #-------------------------- URLS OF DESIGNATION------------------------------------------------------------------

    path('designation_list/', views.designation_list, name='designation_list'),
    path('designation_add/', views.designation_add, name='designation_add'),
    path('designation_edit/<int:designation_id>/', views.designation_edit, name='designation_edit'),


]