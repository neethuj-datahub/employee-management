from django import forms
from .models import Department,Designation



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'description']  # List the fields you want to include


# class DesignationForm(forms.ModelForm):
#     class Meta:
#         model = Designation
#         fields = ['designation_name', 'description', 'department']  # List the fields you want to include
class DesignationForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        empty_label='Select a Department',
        required=True
    )

    class Meta:
        model = Designation
        fields = ['designation_name', 'description', 'department']
