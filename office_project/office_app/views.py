from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


try:
    
    from .ml_predictor import SalaryPredictor
    predictor = SalaryPredictor()
except ImportError:
    
    print("Warning: ml_predictor.py not found.")
    predictor = None
except Exception as e:
    
    print(f"Warning: Could not load ML predictor: {e}")
    predictor = None


def employee_list(request):
    """Display all employees"""
    employees = Employee.objects.all()
    
    
    total = employees.count()
    with_salary = employees.filter(salary__isnull=False).count()
    without_salary = employees.filter(salary__isnull=True).count()
    
    context = {
        'employees': employees,
        'total': total,
        'with_salary': with_salary,
        'without_salary': without_salary,
    }
    return render(request, 'office_app/employee_list.html', context)


def employee_detail(request, employee_id):
    """Display single employee details"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    context = {
        'employee': employee,
        'skills_list': employee.get_skills_list(),
    }
    return render(request, 'office_app/employee_detail.html', context)


def predict_salary(request, employee_id):
    """Predict salary for a single employee"""
    employee = get_object_or_404(Employee, employee_id=employee_id)
    
    if predictor is None:
        messages.error(request, "ML Predictor not available. Check pickle files.")
        return redirect('employee_detail', employee_id=employee_id)
    
    try:
        # Predict salary
        predicted_salary = predictor.predict_salary(
            grade=employee.grade,
            skills_str=employee.skills,
            department_id=employee.department_id,
            designation_id=employee.designation_id
        )
        
       
        employee.salary = predicted_salary
        employee.save()
        
        messages.success(request, f"Salary predicted: ${predicted_salary:,.2f}")
        
    except Exception as e:
        messages.error(request, f"Prediction failed: {str(e)}")
    
    return redirect('employee_detail', employee_id=employee_id)


def predict_all_salaries(request):
    """Predict salaries for all employees without salary"""
    if predictor is None:
        messages.error(request, "ML Predictor not available. Check pickle files.")
        return redirect('employee_list')
    
    employees_without_salary = Employee.objects.filter(salary__isnull=True)
    count = employees_without_salary.count()
    
    if count == 0:
        messages.info(request, "All employees already have salaries.")
        return redirect('employee_list')
    
    success_count = 0
    
    for employee in employees_without_salary:
        try:
            predicted_salary = predictor.predict_salary(
                grade=employee.grade,
                skills_str=employee.skills,
                department_id=employee.department_id,
                designation_id=employee.designation_id
            )
            
            employee.salary = predicted_salary
            employee.save()
            success_count += 1
            
        except Exception as e:
            print(f"Failed to predict for {employee.employee_id}: {e}")
    
    messages.success(request, f"Successfully predicted salaries for {success_count}/{count} employees.")
    return redirect('employee_list')
