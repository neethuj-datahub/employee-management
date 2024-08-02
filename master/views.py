from django.shortcuts import render, redirect , get_object_or_404
from .database_query import get_all_departments,get_all_designations
from datetime import datetime
from django.db import connection
from django.contrib import messages
from .models import Department,Designation  # Import your model
from django.contrib.auth.decorators import login_required
from .forms import DepartmentForm,DesignationForm
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import pandas as pd # type: ignore
import pandas as pd
from django.utils import timezone


def dashboard(request):
    return render(request, 'dashboard.html')

#-------------------------DEPARTMENT------------------------------------------------------------------------

# ---------------------- LIST DEPARTMENT FUNCTION --------------------------------------

def department_list(request):
    departments = get_all_departments()
    return render(request, 'department_list.html', {'departments': departments})

#--------------------- Add Department ----------------------------------------------------

def department_add(request):
    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        description = request.POST.get('description')
        created_at = datetime.now()
        created_by = request.user
        if department_name and description:
            Department.objects.create(
                department_name=department_name,
                description=description,
                created_at=created_at.now(),  
                created_by=created_by       
            )
            messages.success(request, 'Department added successfully!')
            return redirect('department_list') 
        else:
            messages.error(request, 'Both department name and description are required.')

    return render(request, 'department-add.html')
    
#---------------------------Edit Department-------------------------------------------------------------------------------#
    
def department_edit(request,department_id):
    department_instance = get_object_or_404(Department, department_id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department_instance)
        if form.is_valid():
            department = form.save(commit=False)
            department.updated_at = datetime.now()  # Set the updated_at field
            department.updated_by = request.user  # Set the updated_by field
            department.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')  # Redirect after saving
        else:
            messages.error(request, 'Both department name and description are required.')

    else:
        form = DepartmentForm(instance=department_instance)
    print("form",form)
    return render(request, 'department-edit.html', {'form': form,'department': department_instance})

#---------------------------View  Department-------------------------------------------------------------------------------#

def department_view(request,department_id):
    department_instance = get_object_or_404(Department, department_id=department_id)
    return render(request, 'department-view.html',{'department': department_instance})

def department_delete(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')  # Redirect to the department list page
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('department_list')
    
#---------------------------Download  Department Template-------------------------------------------------------------------------------#

def download_template(request):
    template_path = finders.find('template/department_template.xlsx')
    if not template_path:
        # Handle the case where the file is not found
        return HttpResponse("File not found", status=404)
    with open(template_path, 'rb') as template_file:
        response = HttpResponse(template_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="department_template.xlsx"'
        return response
    

#---------------------------Upload Department Details-------------------------------------------------------------------------------#

def bulk_upload(request):
    
        # Check file type
        uploaded_file = request.FILES.get('upload_file')
        if not uploaded_file.name.endswith(('.xls', '.xlsx')):
            raise ValidationError("Invalid file format. Only .xls and .xlsx files are supported.")
        

        df = pd.read_excel(uploaded_file)
        if uploaded_file:
            for index, row in df.iterrows():
                    department_name = row.get('Department Name')
                    description = row.get('Description')
                    created_by = request.user
                    created_at =  timezone.now()
                    Department.objects.update_or_create(
                        department_name=department_name,  # Adjust lookup as needed
                        defaults={
                            'description': description,
                            'created_at': created_at,
                            'created_by': created_by
                        }
                    ) # Replace with your actual success URL
            

            messages.success(request, 'Successfully Added !')
            return redirect('department_list')
        return render(request, 'department-add.html')
            
#---------------------------Export Department Details-------------------------------------------------------------------------------#

def export_departments(request):
    # Use the get_all_departments function to retrieve the department data
    departments = get_all_departments()
    for index, department in enumerate(departments, start=1):
        department['Sl.No'] = index
    # Convert the data to a DataFrame
    df = pd.DataFrame(departments)
    df = df[['Sl.No', 'department_name', 'description']]
    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=departments.xlsx'

    # Write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Departments')

    return response

#---------------------------END OF DEPARTMENT-------------------------------------------------------------------------------#

#---------------------------DESIGNATION-------------------------------------------------------------------------------#

# ---------------------- List Designation --------------------------------------

def designation_list(request):
    designations = get_all_designations()
    departments_all = get_all_departments()
    # dept_name = departments_all.department_name
    print("DESIGNATIONSSSSSSSSSSSSSS:",designations)
    return render(request, 'designation_list.html', {'designations': designations})

#--------------------- Add Designation ----------------------------------------------------

def designation_add(request):
    if request.method == 'POST':
        designation_name = request.POST.get('designation_name')
        description = request.POST.get('description')
        created_at = datetime.now()
        created_by = request.user
        department_id = request.POST.get('department_id')
        
        if designation_name and description:
            Designation.objects.create(
                designation_name=designation_name,
                description=description,
                created_at=created_at,  
                created_by=created_by,
                department_id = department_id,   
            )
            messages.success(request, 'Designation added successfully!')
            return redirect('designation_list') 
        else:
            messages.error(request, 'Both Designation name and description are required.')
    
    departments = Department.objects.all().values('department_id', 'department_name')
    return render(request, 'designation_add.html',{'depts':departments})
    
#---------------------------Edit Designation-------------------------------------------------------------------------------#
    
def designation_edit(request,designation_id):
    designation_instance = get_object_or_404(Designation, designation_id=designation_id)
    departments = Department.objects.all().values('department_id', 'department_name')
    current_department_id = designation_instance.department_id
    current_department_name = designation_instance.department.department_name if designation_instance.department else None
    print("HELLO")
    if request.method == 'POST':
        print("Request POST Data:", request.POST)
        form = DesignationForm(request.POST, instance=designation_instance)
        if form.is_valid():
            print("................")
            selected_department_id = form.cleaned_data['department']
            selected_department = Department.objects.get(pk=selected_department_id)
            designation = form.save(commit=False)
            designation.department = selected_department
            designation.updated_at = datetime.now()  # Set the updated_at field
            designation.updated_by = request.user  # Set the updated_by field
            designation.save()
            print("SAVEDDDDDDD")
            messages.success(request, 'Designation updated successfully!')
            return redirect('designation_list')  # Redirect after saving
        else:
            print("Form Errors:", form.errors)
            messages.error(request, 'Both designation name and description are required.')

    else:
        form = DesignationForm(instance=designation_instance)

    
    return render(request, 'designation_edit.html', {'form': form,'designation': designation_instance,'departments': departments,'current_department_name': current_department_name,'current_department_id':current_department_id })