from django.contrib import admin

# Register your models here.
# tracker/admin.py

from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'status', 'due_date', 'created_at')
    list_filter = ('status', 'due_date')
    search_fields = ('title', 'description', 'assigned_to__username')
