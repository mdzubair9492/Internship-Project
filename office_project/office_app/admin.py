from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'department', 'designation', 
                    'grade', 'salary', 'status']
    list_filter = ['department', 'grade', 'status', 'role']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'email', 'first_name', 'last_name', 
                      'phone', 'address', 'gender', 'date_of_birth')
        }),
        ('Employment Details', {
            'fields': ('employee_id', 'role', 'department', 'department_id',
                      'designation', 'designation_id', 'position', 'grade', 
                      'skills', 'hire_date', 'status')
        }),
        ('Salary', {
            'fields': ('salary',),
            'description': 'Salary is predicted by ML model. Edit manually if needed.'
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
