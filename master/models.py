from django.db import models


# master/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(null=True, blank=True)  # Automatically updates on save
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='%(class)s_updated',  on_delete=models.SET_NULL, null=True,)
    
    class Meta:
        abstract = True

class Department(TimeStampedModel):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        db_table = 'department'

    
    
    def get_instance(self):
        return self


class Designation(TimeStampedModel):
    designation_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    designation_name = models.CharField(max_length=100)
    description =  models.TextField()

    class Meta:
        db_table = 'designation'
    def get_instance(self):
        return self