from django.contrib import admin
from django.contrib import admin
from .models import Student, Course, CourseCatalog

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(CourseCatalog)

# Register your models here.
