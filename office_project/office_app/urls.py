from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),

    
    path('employee/<str:employee_id>/', views.employee_detail, name='employee_detail'),

    
    path('employee/<str:employee_id>/predict/', views.predict_salary, name='predict_salary'),

    path('predict-all/', views.predict_all_salaries, name='predict_all_salaries'),
]
