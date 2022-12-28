from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    pass

# Register your models here.


admin.site.register(Task, TaskAdmin)