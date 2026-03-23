from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import StudentPrediction
import joblib
import os
from django.conf import settings

# Load the AI model
MODEL_PATH = os.path.join(settings.BASE_DIR, 'predictor', 'student_model.pkl')
model = joblib.load(MODEL_PATH)

# --- AUTHENTICATION VIEWS ---

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('login') 
    
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('user_role') 

        if password != confirm_password:
            context['error'] = "Passwords do not match!"
        elif User.objects.filter(username=email).exists():
            context['error'] = "An account with this email already exists."
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            login(request, user)
            
            if role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('teacher_dashboard')
                
    return render(request, 'predictor/signup.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('teacher_dashboard') 
        
    context = {}
    if request.method == 'POST':
        user_email = request.POST.get('username')
        user_pass = request.POST.get('password')
        role = request.POST.get('user_role') 
        
        user = authenticate(request, username=user_email, password=user_pass)

        if user is not None:
            login(request, user)
            if role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('teacher_dashboard')
        else:
            context['error'] = "Invalid email or password."
            
    return render(request, 'predictor/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

# --- TEACHER VIEWS ---

@login_required(login_url='login')
def teacher_dashboard(request):
    students = StudentPrediction.objects.all().order_by('-created_at')
    return render(request, 'predictor/teacher_dashboard.html', {'students': students})

@login_required(login_url='login')
def high_risk_dashboard(request):
    at_risk_students = StudentPrediction.objects.filter(is_at_risk=True).order_by('-created_at')
    
    for student in at_risk_students:
        if student.learning_style == 'Visual':
            student.intervention_plan = "Provide mind maps, color-coded notes, and infographic study guides."
        elif student.learning_style == 'Auditory':
            student.intervention_plan = "Recommend recorded lectures, study groups, and reading notes aloud."
        elif student.learning_style == 'Kinesthetic':
            student.intervention_plan = "Introduce hands-on projects, interactive labs, and frequent short study breaks."
        else: 
            student.intervention_plan = "Provide supplementary reading materials and require written summaries."

    return render(request, 'predictor/high_risk.html', {'at_risk_students': at_risk_students})

@login_required(login_url='login')
def add_student(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name') # MUST BE THE STUDENT'S EMAIL
        attendance = float(request.POST.get('attendance'))
        study_hours = float(request.POST.get('study_hours'))
        online_courses = float(request.POST.get('online_courses'))
        assignment_rate = float(request.POST.get('assignment_rate'))
        learning_style = request.POST.get('learning_style')

        input_data = [[attendance, study_hours, online_courses, assignment_rate]]
        prediction = model.predict(input_data)[0]
        is_at_risk = bool(prediction == 1)

        StudentPrediction.objects.create(
            student_name=name, attendance_rate=attendance, study_hours=study_hours, 
            online_courses=online_courses, assignment_rate=assignment_rate, 
            learning_style=learning_style, is_at_risk=is_at_risk
        )

        context['result'] = "At Risk" if is_at_risk else "On Track"
        context['intervention'] = "Data saved! Check the High Risk dashboard for strategy." if is_at_risk else "Student added successfully."

    return render(request, 'predictor/add_student.html', context)

# --- STUDENT VIEWS ---

@login_required(login_url='login')
def student_dashboard(request):
    # Fetch exactly matching data or return None
    student_record = StudentPrediction.objects.filter(student_name=request.user.email).order_by('-created_at').first()
    return render(request, 'predictor/student_dashboard.html', {'student': student_record})