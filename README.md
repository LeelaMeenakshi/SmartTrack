# SmartTrack – Academic Credit & Course Planning System

SmartTrack is a web application that helps B.Tech students track their academic progress, monitor basket-wise credits, and plan future semesters.
It is built specifically around IIT Gandhinagar’s curriculum structure, supporting batch-wise graduation requirements, discipline-specific baskets, and IITGN’s grading system.
\*\*Smart Track is structured according to curriculum and requirements mentioned from the batch of 2025-26.

## Features

-> User authentication (Signup / Login / Logout)
-> Interactive Dashboard with dynamic credit progress and graduation tracking
-> Basket-wise academic requirement tracking
-> Semester-wise course history with SPI calculation
-> Semester Planner
-> Reports page with academic summary
-> Dynamic semester performance visualization using Chart.js

## Tech Stack

-> Backend: Django
-> Frontend: HTML, CSS
-> Database: PostgreSQL (SQLite used during development)
-> Deployment: Railway
-> Charts: Chart.js

## Setup and Installation Instructions

1. Clone the repository

```bash
git clone https://github.com/LeelaMeenakshi/SmartTrack.git
cd SmartTrack
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/Scripts/Activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run migrations

```bash
python manage.py migrate
```

5. Start the development server

```bash
python manage.py runserver
```

## Links

-> Live URL: https://web-production-fac08c.up.railway.app/
-> GitHub Repository: https://github.com/LeelaMeenakshi/SmartTrack.git

## How to use

1. Sign up / Login
2. Add your completed courses semester-wise
3. Select the appropriate basket for each course
4. View progress on the Dashboard and Basket Tracking page
5. Use the Semester Planner to plan upcoming courses

## Notes

-> Basket assignment is intentionally left to the student. According to IITGN’s curriculum, some courses can belong to different baskets depending on the student’s situation (especially electives and certain open courses).  
-> SmartTrack allows the student to choose the appropriate basket while adding a course. This gives more accurate progress tracking than fully automatic assignment.

**Pass/Fail courses**
Pass/Fail courses (like Foundation Programme, GE Courses) when selected, count toward credits but are excluded from GPA calculation.

**Basket & Sub-basket Logic**
In IITGN’s curriculum, some baskets contain sub-baskets.
**Example:**  
In the AI discipline, the **Core Electives** basket has a sub-basket called **CSE basket**.
SmartTrack handles this as follows:
-> When a course is added to a **sub-basket** (e.g. CSE), its credits are automatically counted towards the **parent basket** (Core Electives) as well.
-> This ensures progress remains accurate at both levels.

**The basic advisory details are clearly shown in the User Guide page once logged in.**
**The details regarding courses in each basket are also written in User GUide page.**

##Author
Leela Meenakshi
[GitHub: https://github.com/LeelaMeenakshi/SmartTrack.git]
