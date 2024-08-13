from django.db import models
import uuid


# master/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='%(class)s_created_by',
        null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)  # Automatically updates on save
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='%(class)s_updated_by',blank=True, null=True)
    
    class Meta:
        abstract = True
#--------------------------------------------models for master ------------------------------------------------------------
class Department(TimeStampedModel):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        db_table = 'department'

    def __str__(self):
        return str(self.department_name) 


class Designation(TimeStampedModel):
    designation_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department,  on_delete=models.PROTECT,)
    designation_name = models.CharField(max_length=100)
    description =  models.TextField()

    class Meta:
        db_table = 'designation'
    def __str__(self):
        return str(self.designation_name) 
    
class Location(TimeStampedModel):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        db_table = 'location'

    def __str__(self):
        return str(self.location_name) 


class Employee(TimeStampedModel):
    employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    join_date = models.DateField(null=True, blank=True)
    employee_no = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=255,null=True, blank=True)
    address = models.CharField(max_length=255,null=True, blank=True)
    emp_start_date = models.DateField(null=True, blank=True)
    emp_end_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    status = models.CharField(max_length=50)
    department = models.ForeignKey(Department, max_length=250, null=True, blank=True, related_name='emp_dep',
                             on_delete=models.SET_NULL)
    designation = models.ForeignKey(Designation, max_length=250, null=True, blank=True, related_name='emp_des',
                             on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, max_length=250, null=True, blank=True, related_name='emp_loc',
                             on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'employee'
    def __str__(self):
        return str(self.name)    
    

class Skills(models.Model):
    skill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=255,null=True, blank=True)

    class Meta:
        db_table = 'skills'
    def __str__(self):
        return str(self.skill_name)   
    



from django.contrib.auth.models import User,AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_TYPES = (
        ('ADMIN', 'ADMIN'),
        ('VIEWER', 'VIEWER'),
    )

    role = models.CharField(max_length=10, choices=ROLE_TYPES)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups' 
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions' 
    )

    def get_instance(self):
        return self