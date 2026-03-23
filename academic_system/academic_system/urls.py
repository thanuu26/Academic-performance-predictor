"""
URL configuration for academic_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from predictor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('', views.login_view, name='login'), 
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Teacher Routes
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/high-risk/', views.high_risk_dashboard, name='high_risk'),
    path('teacher/add-student/', views.add_student, name='add_student'),
    
    # Student Routes
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]