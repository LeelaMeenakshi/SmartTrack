from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student, Course, CourseCatalog
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import Student, CourseCatalog, CompletedCourse
from collections import defaultdict
from django.http import JsonResponse
def signup_view(request):
    

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=email).exists():

            messages.error(
                request,
                'Account already exists'
            )

            return redirect('signup')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        login(request, user)

        return redirect('dashboard')

    return render(
        request,
        'signuppage.html'
    )


def login_view(request):

    if request.method == 'POST':

        email=request.POST.get('email')
        password=request.POST.get('password')

        user=authenticate(
            request,
            username=email,
            password=password
        )

        if user:

            login(request,user)

            return redirect('dashboard')

        messages.error(
            request,
            'Invalid credentials'
        )

        return redirect('login')

    return render(
        request,
        'loginpage.html'
    )

from .models import Student
from .models import Course
@ensure_csrf_cookie
def dashboard_view(request):
    student = Student.objects.first()
    courses = Course.objects.filter(
        student = student
    )
    catalog_courses = CourseCatalog.objects.all()[:10]
    print(catalog_courses)

    return render(
        request,
        'dashboard.html',
        {
            'user':request.user,
            'student': student,
            'courses': courses,
            'catalog_courses': catalog_courses
        }
    )


def logout_view(request):

    logout(request)

    return redirect('index')


def index_view(request):

    return render(
        request,
        'landingpage copy.html'
    )

def courses_view(request):
    return render(
        request,
        'mycourses.html'
    )

def basket(request):
    return render(request,'basket.html')

def planner_view(request):
    return render(request,'semplanner.html')

def reports(request):
    return render(request,'history.html')


def search_course(request):
    query = request.GET.get("q")
    courses = CourseCatalog.objects.filter(
        Q(course_code__icontains= query) |
        Q(course_name__icontains= query)
    )
    results= []
    for course in courses:
        dic = {"course_code":course.course_code,
               "course_name":course.course_name
               }
        results.append(dic)
    return JsonResponse({
        "courses":results
    })

def save_semester(request):
    data = json.loads(request.body)
    print(data)
    student = Student.objects.first()
    semester = data["semester"]
    CompletedCourse.objects.filter(
        student = student,
        semester = semester
    ).delete()
    for course in data["courses"]:
        catalog_course = CourseCatalog.objects.get(
            course_code = course["course_code"]
        )

        CompletedCourse.objects.create(
            student = student,
            semester = data["semester"],
            grade = course["grade"],
            basket=course["basket"],
            course = catalog_course
        )

    return JsonResponse({
        "message":"Saved successfully"
    })

def get_semesters(request):
    student = Student.objects.first()
    completed_courses = CompletedCourse.objects.filter(
        student = student
    )
    semesters= {}
    for course in completed_courses:
        semester = course.semester
        if semester not in semesters:
            semesters[semester]= []
        course_data = {
            "course_code": course.course.course_code,
            "course_name": course.course.course_name,
            "grade": course.grade,
            "basket": course.basket,
            
        }
        semesters[semester].append(course_data)
    return JsonResponse({
        "semesters": semesters
    })

def remove_course(request):
    data = json.loads(request.body)
    print(data)
    student = Student.objects.first()
    semester = data["semester"]
    course_code = data["course_code"]
    completed_course = CompletedCourse.objects.get(
        student=student,
        semester=semester,
        course__course_code=course_code
    )
    completed_course.delete()
    return JsonResponse({
        "message": "Course removed successfully"
    })
BASKET_REQUIREMENTS = {
    "Mandatory": 32,
    "Maths": 10,
    "Science": 12,   # Placeholder for now
    "HSS": 20,       # Placeholder
    "MSE": 3,        # We'll update later
}
MANDATORY_PREFIXES = {
    "ES 101",
    "ES 112",
    "ES 114",
    "ES 115",
    "ES 116",
    "ES 117",
    "ES 119",
    "ES 243",
    "BS 192",
}
def basket_analysis(request):
    student = Student.objects.first()
    completed_courses = CompletedCourse.objects.filter(student= student)
    progress={}
    # for completed in completed_courses:
    #     code = completed.course.course_code
    #     credits = completed.course.credits
    #     print(code,credits)
    for basket,required in BASKET_REQUIREMENTS.items():
      progress[basket] = {
        "completed": 0,
        "required": required,
      } 
    for completed in completed_courses:
        code = completed.course.course_code
        credits = completed.course.credits
        for mandatory in MANDATORY_PREFIXES: 
            if code.startswith(mandatory):
                progress["Mandatory"]["completed"] += credits
                break
   
        if code.startswith("MA"):
            progress["Maths"]["completed"]+=credits
        elif code.startswith("PH") or code.startswith("CH"):
            progress["Science"]["completed"]+=credits
        elif code.startswith("HS") :
            progress["HSS"]["completed"]+=credits
        elif code.startswith("MSE") :
            progress["MSE"]["completed"]+=credits
        print(code,credits)
        
        
    return JsonResponse(progress) 

def history_data(request):
    student = Student.objects.first()
    completed_courses = CompletedCourse.objects.filter(student= student)
    history ={}
    for sem in range(1,9):
        history[sem]={
            "credits":0,
            "courses": 0,
            "spi": 0,
            "grade_points": 0,
            "course_list": [],
        }
    for completed in completed_courses:
        sem = completed.semester

        history[sem]["credits"] += completed.course.credits
        history[sem]["courses"] += 1
        history[sem]["grade_points"]+=(completed.grade*completed.course.credits)
        history[sem]["course_list"].append({
            "name": completed.course.course_name,
            "code": completed.course.course_code,
            "credits": completed.course.credits,
            "grade": completed.grade,
            "basket": completed.basket,
        })
    
    for sem in history:
        if history[sem]["credits"]>0:
            history[sem]["spi"]= round(
                history[sem]["grade_points"] /history[sem]["credits"],2
            )

    return JsonResponse(history)

# Create your views here.
