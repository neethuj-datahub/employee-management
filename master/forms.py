from django import forms
from .models import Department,Designation,Location


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

