from django.shortcuts import render, redirect , get_object_or_404
from .database_query import get_all_departments,get_all_designations,get_all_locations
from datetime import datetime
from django.db import connection
from django.contrib import messages
from .models import Department,Designation,Location # Import your model
from django.contrib.auth.decorators import login_required
from .forms import DepartmentForm,DesignationForm,LocationForm
import os
from django.conf import settings
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import pandas as pd # type: ignore
import pandas as pd
from django.utils import timezone
import openpyxl
from openpyxl.styles import PatternFill
from django.http import HttpResponse
from io import BytesIO




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
            department.updated_at = datetime.now()  
            department.updated_by = request.user  
            department.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('department_list')  #
        else:
            messages.error(request, 'Both department name and description are required.')

    else:
        form = DepartmentForm(instance=department_instance)
    return render(request, 'department-edit.html', {'form': form,'department': department_instance})

#---------------------------View  Department-------------------------------------------------------------------------------#

def department_view(request,department_id):
    department_instance = get_object_or_404(Department, department_id=department_id)
    return render(request, 'department-view.html',{'department': department_instance})

#---------------------------Delete  Department-------------------------------------------------------------------------------#


def department_delete(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully!')
        return redirect('department_list')  
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
                        department_name=department_name,  
                        defaults={
                            'description': description,
                            'created_at': created_at,
                            'created_by': created_by
                        }
                    ) 
            

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

#######################################################################################################################################################

#---------------------------DESIGNATION-------------------------------------------------------------------------------#

# ---------------------- List Designation --------------------------------------

def designation_list(request):
    designations = get_all_designations()
    departments_all = get_all_departments()
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
    
def designation_edit(request, designation_id):
    designation_instance = get_object_or_404(Designation, pk=designation_id)
    departments = Department.objects.all()  # Get all departments for the dropdown
    current_department_id = designation_instance.department.pk if designation_instance.department else None
    current_department_name = designation_instance.department.department_name if designation_instance.department else None
    
    if request.method == 'POST':
        form = DesignationForm(request.POST, instance=designation_instance)
        if form.is_valid():
            # Save the form data
            designation = form.save(commit=False)
            designation.updated_at = timezone.now() 
            designation.updated_by = request.user  
            designation.save()
            
            messages.success(request, 'Designation updated successfully!')
            return redirect('designation_list') 
        else:
            messages.error(request, 'Both designation name and description are required.')

    else:
        form = DesignationForm(instance=designation_instance)

    
    return render(request, 'designation_edit.html', {'form': form,'designation': designation_instance,'departments': departments,'current_department_name': current_department_name,'current_department_id':current_department_id })



#---------------------------View  Designation-------------------------------------------------------------------------------#

def designation_view(request,designation_id):
    designation_instance = get_object_or_404(Designation, designation_id=designation_id)
    dept_obj = Department.objects.filter(department_id = designation_instance.department.department_id).first()
    dept_name = dept_obj.department_name
    return render(request, 'designation_view.html',{'designation': designation_instance,'dept_name':dept_name})

#---------------------------Delete  Designation-------------------------------------------------------------------------------#

def designation_delete(request, designation_id):
    designation = get_object_or_404(Designation, designation_id=designation_id)
    if request.method == 'POST':
        designation.delete()
        messages.success(request, 'Designation deleted successfully!')
        return redirect('designation_list')  
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('designation_list')
    

#---------------------------Download  Designation Template-------------------------------------------------------------------------------#


def designation_download_template(request):
    departments = Department.objects.values_list('department_name', flat=True)
    if not departments:
        departments = ["No departments available"]  # Fallback if no departments exist

    # Create a new workbook and add worksheets
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Template"

    # Add column headers for data entry
    ws['A1'] = "Department Name"
    ws['B1'] = "Designation Name"
    ws['C1'] = "Description"

    # Highlighting style for instructions
    highlight_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

    # Add instructions to the same sheet (ws) but after the columns
    instruction_start_coloumn = 4  # Row to start instructions after data columns
    ws[f'D{instruction_start_coloumn}'] = "Instructions:"
    ws[f'E{instruction_start_coloumn + 1}'] = "Please include only departments listed in the 'Department List' sheet."

    # Apply highlighting to the instruction cells
    ws[f'D{instruction_start_coloumn}'].fill = highlight_fill
    ws[f'E{instruction_start_coloumn + 1}'].fill = highlight_fill

    # Add a new worksheet for the department list
    ws_list = wb.create_sheet(title="Department List")

    # Add instructions in the new sheet
    ws_list['A1'] = "List of Departments (Include only these in the 'Department Name' column)"
    ws_list['A1'].fill = highlight_fill

    # Add department names to the new sheet
    for idx, dept in enumerate(departments, start=2):
        ws_list[f'A{idx}'] = dept

    # Save the workbook to a BytesIO object
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Serve the file as a downloadable response
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="designation_template.xlsx"'
    return response


#---------------------------Bulk Upload Designation -------------------------------------------------------------------------------#


def designation_bulk_upload(request):
    
     if request.method == 'POST':
        uploaded_file = request.FILES.get('upload_file')
        
        if not uploaded_file or not uploaded_file.name.endswith(('.xls', '.xlsx')):
            messages.error(request, "Invalid file format. Only .xls and .xlsx files are supported.")
            return render(request, 'designation_add.html')

        try:
            df = pd.read_excel(uploaded_file)  # Skip the first 3 rows where headers are assumed to be
        except Exception as e:
            messages.error(request, f"Error reading the file: {str(e)}")
            return render(request, 'designation_add.html')

        if df.empty:
            messages.error(request, 'The uploaded file is empty or does not contain valid data.')
            return render(request, 'designation_add.html')

        # Fetch existing department names for validation
        existing_departments = set(Department.objects.values_list('department_name', flat=True))

        # Track rows with warnings
        warnings = []

        for index, row in df.iterrows():
            department_name = row.get('Department Name')
            designation_name = row.get('Designation Name')
            description = row.get('Description')
            created_by = request.user
            created_at = timezone.now()

            # Skip rows with missing or invalid data
            if pd.isna(department_name) or not department_name.strip():
                warnings.append(f"Row {index + 1}: Department name is missing or invalid. This row will be ignored.")
                continue

            if pd.isna(designation_name) or not designation_name.strip():
                warnings.append(f"Row {index + 1}: Designation name is missing or invalid. This row will be ignored.")
                continue

            if pd.isna(description) or not description.strip():
                warnings.append(f"Row {index + 1}: Description is missing or invalid. This row will be ignored.")
                continue

            # Check if the department is valid
            if department_name not in existing_departments:
                warnings.append(f"Row {index + 1}: Department '{department_name}' is not in the department list. This row will be ignored.")
                continue

            # Get department instance
            try:
                department_instance = Department.objects.get(department_name=department_name)
            except Department.DoesNotExist:
                warnings.append(f"Row {index + 1}: Department '{department_name}' not found. This row will be ignored.")
                continue

            # Update or create the designation
            try:
                Designation.objects.update_or_create(
                    designation_name=designation_name,
                    defaults={
                        'description': description,
                        'created_at': created_at,
                        'created_by': created_by,
                        'department_id': department_instance.department_id  # Use 'id' to refer to the primary key
                    }
                )
            except Exception as e:
                warnings.append(f"An error occurred while processing row {index + 1}: {str(e)}")

        # Provide feedback to the user
        if warnings:
            for warning in warnings:
                messages.warning(request, warning)
        else:
            messages.success(request, 'Successfully added/updated designations!')

        return redirect('designation_list')

     return render(request, 'designation_add.html')

#---------------------------Export Designation Details-------------------------------------------------------------------------------#

def export_designations(request):
    # Use the get_all_designation function to retrieve the designation data
    designations = get_all_designations()
    for index, designation in enumerate(designations, start=1):
        designation['Sl.No'] = index
    # Convert the data to a DataFrame
    df = pd.DataFrame(designations)
    df = df[['Sl.No', 'designation_name', 'description','department_name']]
    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=designations.xlsx'

    # Write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Designations')

    return response

##########################################################################################################################################

#--------------------------------------------LOCATIONS---------------------------------------------------------------------------------------

# ---------------------- List Locations --------------------------------------

def location_list(request):
    locations = get_all_locations()
    return render(request, 'location_list.html', {'locations': locations})

#--------------------- Add Location ----------------------------------------------------

def location_add(request):
    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        description = request.POST.get('description')
        created_at = datetime.now()
        created_by = request.user
        if location_name and description:
            Location.objects.create(
                location_name=location_name,
                description=description,
                created_at=created_at,  
                created_by=created_by       
            )
            messages.success(request, 'Location added successfully!')
            return redirect('location_list') 
        else:
            messages.error(request, 'Both Location name and description are required.')

    return render(request, 'location_add.html')



#---------------------------Edit Location-------------------------------------------------------------------------------#
    
def location_edit(request,location_id):
    location_instance = get_object_or_404(Location, location_id=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location_instance)
        if form.is_valid():
            location = form.save(commit=False)
            location.updated_at = datetime.now()  
            location.updated_by = request.user  
            location.save()
            messages.success(request, 'Location updated successfully!')
            return redirect('location_list')  
        else:
            messages.error(request, 'Both Location name and description are required.')

    else:
        form = LocationForm(instance=location_instance)
    return render(request, 'location_edit.html', {'form': form,'location': location_instance})


#---------------------------View  Location-------------------------------------------------------------------------------#

def location_view(request,location_id):
    location_instance = get_object_or_404(Location, location_id=location_id)
    return render(request, 'location_view.html',{'location': location_instance})


#---------------------------Delete  Location-------------------------------------------------------------------------------#


def location_delete(request, location_id):
    location = get_object_or_404(Location, location_id=location_id)
    if request.method == 'POST':
        location.delete()
        messages.success(request, 'Location deleted successfully!')
        return redirect('location_list')  
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('location_list')
    download_location_template

#---------------------------Download  Location Template-------------------------------------------------------------------------------#

def download_location_template(request):
    template_path = finders.find('template/location_template.xlsx')
    if not template_path:
        # Handle the case where the file is not found
        return HttpResponse("File not found", status=404)
    with open(template_path, 'rb') as template_file:
        response = HttpResponse(template_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="location_template.xlsx"'
        return response
    

#---------------------------Upload location Details-------------------------------------------------------------------------------#

def location_bulk_upload(request):

        # Check file type
        uploaded_file = request.FILES.get('upload_file')
        if not uploaded_file.name.endswith(('.xls', '.xlsx')):
            raise ValidationError("Invalid file format. Only .xls and .xlsx files are supported.")
            

        df = pd.read_excel(uploaded_file)
        if uploaded_file:
            for index, row in df.iterrows():
                    location_name = row.get('Location Name')
                    description = row.get('Description')
                    created_by = request.user
                    created_at =  timezone.now()
                    Location.objects.update_or_create(
                        location_name=location_name,  
                        defaults={
                            'description': description,
                            'created_at': created_at,
                            'created_by': created_by
                        }
                    ) 
            

            messages.success(request, 'Successfully Added !')
            return redirect('location_list')
        return render(request, 'location_list.html')
            
#---------------------------Export Location Details-------------------------------------------------------------------------------#

def export_locations(request):
    # Use the get_all_locations function to retrieve the department data
    locations = get_all_locations()
    for index, location in enumerate(locations, start=1):
        location['Sl.No'] = index
    # Convert the data to a DataFrame
    df = pd.DataFrame(locations)
    df = df[['Sl.No', 'location_name', 'description']]
    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Locations.xlsx'

    # Write the DataFrame to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Locations')

    return response

