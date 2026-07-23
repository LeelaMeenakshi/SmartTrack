from .models import CompletedCourse

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

    return progress

