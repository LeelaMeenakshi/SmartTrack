from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20, blank=True, default="")
    discipline = models.CharField(max_length=50, default="CSE")
    batch_year = models.CharField(max_length=20, default="2025-26")
    total_credits_required = models.IntegerField(default=173)

    def __str__(self):
        return self.name


class Course(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20)
    credits = models.IntegerField()
    grade = models.CharField(max_length=5)
    semester = models.IntegerField()
    basket = models.CharField(max_length=50)

    def __str__(self):
        return self.course_name
    
class CourseCatalog(models.Model):
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()
    basket = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.course_code} - {self.course_name}"
    
class CompletedCourse(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    semester = models.IntegerField()
    grade = models.FloatField()
    course= models.ForeignKey(CourseCatalog, on_delete = models.CASCADE)
    basket = models.CharField(max_length=50)

class SemesterPlan(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    course = models.ForeignKey(CourseCatalog, on_delete=models.CASCADE)
    basket = models.CharField(max_length=50)
    class Meta:
        constraints= [
            models.UniqueConstraint(
                fields = ['student', 'course'],
                name = "unique_student_course",
            )
        ]

# Create your models here.
