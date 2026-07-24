from .models import CompletedCourse, SemesterPlan

from .basket_config import COMMON_BASKETS, BRANCH_BASKETS
def calculate_progress(student):
    completed_courses = CompletedCourse.objects.filter(student=student)
    branch= student.discipline
    all_baskets = {}
    all_baskets.update(COMMON_BASKETS)
    all_baskets.update(BRANCH_BASKETS[branch])
    progress = {}
    for basket, required in all_baskets.items():
        progress[basket] = {
            "required": required,
            "completed": 0,
            "planned" : 0,
            "course_list": [],
        }

    for completed in completed_courses:
        course = completed.course
        basket = completed.basket
        credits = course.credits

        progress[basket]["completed"] += credits
        progress[basket]["course_list"].append({
            "code": course.course_code,
            "name": course.course_name,
            "credits": course.credits,
            "grade": completed.grade,
        })

        if basket == "Theory and Algorithms Basket" or basket == "Systems Basket":
            progress["CSE Discipline Electives"]["completed"] += credits
            progress["CSE Discipline Electives"]["course_list"].append({
                "code": course.course_code,
                "name": course.course_name,
                "credits": course.credits,
                "grade": completed.grade,
            })

        elif basket == "Design or Applications" or basket == "General CE electives":
            progress["CE Discipline Electives"]["completed"] += credits
            progress["CE Discipline Electives"]["course_list"].append({
                "code": course.course_code,
                "name": course.course_name,
                "credits": course.credits,
                "grade": completed.grade,
            })

        elif basket == "CSE Basket":
            progress["AI Discipline Electives"]["completed"] += credits
            progress["AI Discipline Electives"]["course_list"].append({
                "code": course.course_code,
                "name": course.course_name,
                "credits": course.credits,
                "grade": completed.grade,
            })

    planned_courses = SemesterPlan.objects.filter(student=student)
    for plan in planned_courses:
        basket = plan.basket
        credits = plan.course.credits
        progress[basket]["planned"] += credits
        if basket == "Theory and Algorithms Basket" or basket == "Systems Basket":
            progress["CSE Discipline Electives"]["planned"] += credits
        elif basket == "Design or Applications" or basket == "General CE electives":
            progress["CE Discipline Electives"]["planned"] += credits
        elif basket == "CSE Basket":
            progress["AI Discipline Electives"]["planned"] += credits

        # print(calculate_progress(student))

    return progress

def calculate_history(student):
    completed_courses = CompletedCourse.objects.filter(student= student)  
    history = {}
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

    available_semesters = []
    for sem in history:
        if history[sem]["credits"]==0:
            available_semesters.append(sem)

    return history, available_semesters