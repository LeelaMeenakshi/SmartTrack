from django.contrib import admin
from django.contrib import admin
from .models import Student, Course, CourseCatalog
from django.contrib import admin
from .models import CompletedCourse

admin.site.register(CompletedCourse)

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseCatalog)

# Register your models here.
