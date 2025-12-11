from django.db import models

class Employee(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('on_leave', 'On Leave'),
    ]
    
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('hradmin', 'HR Admin'),
    ]
    
    GRADE_CHOICES = [
        (1, 'Grade 1'),
        (2, 'Grade 2'),
        (3, 'Grade 3'),
        (4, 'Grade 4'),
    ]
    
    # Auto-increment ID
    id = models.AutoField(primary_key=True)
    
    # User credentials
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    
    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    
    # Employment info
    employee_id = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100)
    department_id = models.IntegerField()
    designation = models.CharField(max_length=100)
    designation_id = models.IntegerField()
    position = models.CharField(max_length=100)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    
    # Skills (comma-separated string)
    skills = models.TextField(help_text="Comma-separated skill IDs (e.g., '8,15,3')")
    
    # Salary (NULL initially, filled by ML)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    hire_date = models.DateField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees'
        managed = False  # Don't let Django manage this table
        ordering = ['employee_id']
    
    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
    
    def get_skills_list(self):
        """Convert skills string to list"""
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
        return []
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
