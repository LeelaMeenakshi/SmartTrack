from django.db import models
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20)
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
    

# Create your models here.
