import csv

from courses.models import CourseCatalog


with open(
    'data/courses.csv',
    encoding='utf-8'
) as file:

    reader = csv.reader(file)

    next(reader)

    for row in reader:

        code = row[0].strip()

        name = row[1].strip()

        credits = int(row[2])

        CourseCatalog.objects.get_or_create(

            course_code=code,

            defaults={

                'course_name': name,

                'credits': credits,

                'basket': 'Unknown'
            }
        )

print("Courses imported")