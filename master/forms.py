from django import forms
from .models import Department,Designation,Location,Employee,Skills
from django.forms import modelformset_factory



#----------------------------department---------------------------------------

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'description'] 

#----------------------------designation---------------------------------------

class DesignationForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label='Select a Department',
        required=True
    )

    class Meta:
        model = Designation
        fields = ['designation_name', 'description', 'department']

#----------------------------location---------------------------------------

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['location_name', 'description']  

#--------------------------- employee ------------------------------------------------------------------------------------


class Date(forms.DateInput):
    input_type = 'date'
    format = '%Y-%m-%d' 
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [ 'join_date', 'employee_no', 'name', 'phone', 'address', 'emp_start_date', 'emp_end_date', 'photo', 'status', 'department', 'designation', 'location']
        widgets = {
            'join_date': Date(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'employee_no': forms.TextInput(attrs={'type': 'text', 'required': 'true'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'emp_start_date': forms.DateInput(attrs={'class': 'form-control', 'required': 'true', 'type': 'date'}),
            'emp_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control','id': 'department-dropdown'}),
            'designation': forms.Select(attrs={'class': 'form-control','id': 'designation-dropdown'}),
            'location': forms.Select(attrs={'class': 'form-control',})
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill_name','description']
        widgets = {
            'skill_name': forms.TextInput(attrs={'type': 'text', 'required': 'true'}),
            'description':forms.TextInput(attrs={'type': 'text', 'required': 'true'}),
        }
        
# Creates a formset for handling multiple Skills entries, allowing for dynamic addition and deletion of skill forms.
SkillFormSet = modelformset_factory(Skills, form=SkillForm, extra=0, can_delete=True)


class ExcelUploadForm(forms.Form):
    file = forms.FileField()