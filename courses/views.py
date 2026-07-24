from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student, Course, CourseCatalog , SemesterPlan
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import Student, CourseCatalog, CompletedCourse
from collections import defaultdict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .helpers import calculate_history, calculate_progress
from django.views.decorators.http import require_POST
import json
def signup_view(request):
    

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        branch = request.POST.get("branch")

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
        Student.objects.create(
            name=name,
            email=email,
            discipline=branch,
            roll_number="",
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

@login_required
def logout_view(request):

    logout(request)

    return redirect('index')


def index_view(request):

    return render(
        request,
        'landingpage copy.html'
    )
@login_required
def courses_view(request):
    return render(
        request,
        'mycourses.html'
    )
from .basket_config import COMMON_BASKETS, BRANCH_BASKETS

@login_required
def planner_view(request):
    student = Student.objects.get(email=request.user.email)
    branch = student.discipline
    all_baskets = {}
    all_baskets.update(COMMON_BASKETS)
    all_baskets.update(BRANCH_BASKETS[branch])
    
    
    history, available_semesters = calculate_history(student)
    completed_credits = sum(history[sem]["credits"] for sem in history)
    completed_ids= CompletedCourse.objects.filter(student=student).values_list('course_id', flat=True)
    planned_ids = SemesterPlan.objects.filter( student=student).values_list("course_id", flat=True)
    planned_courses = SemesterPlan.objects.filter(student=student)
    planned_credits= 0
    for plan in planned_courses:
        planned_credits += plan.course.credits

    total_credits = completed_credits + planned_credits

    if planned_credits < 20:
        load_status = "Below Recommended"
    elif planned_credits <=24:
        load_status = "In recommended range"
    elif planned_credits >28:
        load_status = "Exceeds default maximum load"
    available_courses= CourseCatalog.objects.exclude(id__in=completed_ids).exclude(id__in=planned_ids)
    print("Completed:", list(completed_ids))
    print("Planned:", list(planned_ids))
    print("Available:", available_courses.count())
    progress = calculate_progress(student)
    print(progress)
    return render(request,'semplanner.html',{
        "student": student,
        "available_semesters":available_semesters,
        "catalog_courses": available_courses,
        "planned_courses": planned_courses,
        "planned_credits": planned_credits,
        "baskets": list(all_baskets.keys()),
        "load_status": load_status,
        "total_credits": total_credits,
        "progress": progress,
    })
@login_required
def reports(request):
    return render(request,'history.html')

@login_required
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
@login_required
def save_semester(request):
    data = json.loads(request.body)
    print(data)
    student = Student.objects.get(email=request.user.email)
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
@login_required
def get_semesters(request):
    student = Student.objects.get(email=request.user.email)
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
@login_required
def remove_course(request):
    data = json.loads(request.body)
    print(data)
    student = Student.objects.get(email=request.user.email)
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
from .basket_config import COMMON_BASKETS, BRANCH_BASKETS
# @login_required
# def basket_analysis(request):
#     student = Student.objects.get(email=request.user.email)
#     branch = student.discipline
#     all_baskets = {}
#     all_baskets.update(COMMON_BASKETS)
#     all_baskets.update(BRANCH_BASKETS[branch])
#     completed_courses = CompletedCourse.objects.filter(student= student)
#     progress={}
#     # for completed in completed_courses:
#     #     code = completed.course.course_code
#     #     credits = completed.course.credits
#     #     print(code,credits)
#     for basket,required in all_baskets.items():
#       progress[basket] = {
#         "completed": 0,
#         "required": required,
#         "course_list": []
#       } 
#     for completed in completed_courses:
#         code = completed.course.course_code
#         credits = completed.course.credits
#         basket = completed.basket
#         progress[basket]["completed"] += credits
#         progress[basket]["course_list"].append({
#             "name": completed.course.course_name,
#             "code": completed.course.course_code,
#             "credits": completed.course.credits,
#             "grade":completed.grade,
#         })
           
        
#     return JsonResponse(progress, safe= False) 

from .basket_config import COMMON_BASKETS, BRANCH_BASKETS
from django.contrib.auth.decorators import login_required

@login_required
def basket(request):

    student = Student.objects.get(email=request.user.email)

    progress = calculate_progress(student)


    cards= []
    for basket,data in progress.items():
        cards.append({
            "name":basket,
            "completed":data["completed"],
            "required":data["required"],
            "course_list":data["course_list"],
            "percentage": round((data["completed"]/data["required"])*100,2) if data["required"]>0 else 0
        })

    return render(
        request,
        "basket.html",
        {
            "student": student,
            "cards": cards,
        }
    )

@login_required
def basket_analysis(request):
    student = Student.objects.get(email=request.user.email)

    progress = calculate_progress(student)

    return JsonResponse(progress, safe=False)

@login_required
@ensure_csrf_cookie
def dashboard_view(request):
    student = Student.objects.get(email=request.user.email)
    branch = student.discipline
    all_baskets = {}
    all_baskets.update(COMMON_BASKETS)
    all_baskets.update(BRANCH_BASKETS[branch])
    
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
            'catalog_courses': catalog_courses,
            "baskets": list(all_baskets.keys())
        }
    )


@login_required
def history_data(request):
    student = Student.objects.get(email=request.user.email)
    completed_courses = CompletedCourse.objects.filter(student= student)
    history,available_semesters = calculate_history(student)

    
    for sem in history:
        if history[sem]["credits"]>0:
            history[sem]["spi"]= round(
                history[sem]["grade_points"] /history[sem]["credits"],2
            )

    return JsonResponse(history)


@login_required
def planner_search_course(request):
    query = request.GET.get("q", "").strip()

    student = Student.objects.get(email=request.user.email)

    completed_ids = CompletedCourse.objects.filter(
        student=student
    ).values_list("course_id", flat=True)

    planned_ids = SemesterPlan.objects.filter(
        student=student
    ).values_list("course_id", flat=True)

    courses = (
        CourseCatalog.objects
        .exclude(id__in=completed_ids)
        .exclude(id__in=planned_ids)
        .filter(
            course_name__icontains=query
        )[:10]
    )

    data = []

    for course in courses:
        data.append({
            "code": course.course_code,
            "name": course.course_name,
            "credits": course.credits,
        })

    return JsonResponse(data, safe=False)

def add_planned_course(request):

    student = Student.objects.get(email=request.user.email)

    data = json.loads(request.body)

    semester = data.get("semester")
    course_code = data.get("course_code")
    basket = data.get("basket")

    course = CourseCatalog.objects.get(course_code=course_code)

    SemesterPlan.objects.create(
        student=student,
        semester=semester,
        course=course,
        basket=basket,
    )

    return JsonResponse({"success": True})

@require_POST
@login_required
def remove_planned_course(request):

    student = Student.objects.get(email=request.user.email)

    data = json.loads(request.body)

    plan_id = data.get("plan_id")

    SemesterPlan.objects.filter(
        id=plan_id,
        student=student
    ).delete()

    return JsonResponse({"success": True})
# Create your views here.
