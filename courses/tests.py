from django.test import TestCase

from .helpers import calculate_credit_summary
from .models import CompletedCourse, CourseCatalog, Student


class RequirementToggleTests(TestCase):
    def test_credit_summary_reflects_toggled_requirements(self):
        student = Student.objects.create(
            name="Toggle Student",
            email="toggle@example.com",
            discipline="CSE",
            total_credits_required=173,
            foundation_program=False,
            ge_course_1=False,
            ge_course_2=False,
        )

        summary = calculate_credit_summary(student)

        self.assertEqual(summary["completed_credits"], 0)
        self.assertEqual(summary["remaining_credits"], 173)

        student.foundation_program = True
        student.ge_course_1 = True
        student.save()

        summary = calculate_credit_summary(student)

        self.assertEqual(summary["completed_credits"], 6)
        self.assertEqual(summary["remaining_credits"], 167)


class CreditSummaryTests(TestCase):
    def test_credit_summary_uses_student_required_credits_and_completed_courses(self):
        student = Student.objects.create(
            name="Test Student",
            email="student@example.com",
            discipline="CSE",
            total_credits_required=173,
            foundation_program=True,
            ge_course_1=True,
            ge_course_2=False,
        )

        course_1 = CourseCatalog.objects.create(
            course_code="CS101",
            course_name="Intro to Computing",
            credits=3,
            basket="Mandatory",
        )
        course_2 = CourseCatalog.objects.create(
            course_code="CS102",
            course_name="Data Structures",
            credits=4,
            basket="Mandatory",
        )

        CompletedCourse.objects.create(
            student=student,
            semester=1,
            grade=8.5,
            course=course_1,
            basket="Mandatory",
        )
        CompletedCourse.objects.create(
            student=student,
            semester=2,
            grade=9.0,
            course=course_2,
            basket="Mandatory",
        )

        summary = calculate_credit_summary(student)

        self.assertEqual(summary["completed_credits"], 11)
        self.assertEqual(summary["required_credits"], 173)
        self.assertEqual(summary["remaining_credits"], 162)
