from django.contrib import admin
from .models import TimeLog, JobGroup

# Register your models here.
admin.site.register(TimeLog)
admin.site.register(JobGroup)
