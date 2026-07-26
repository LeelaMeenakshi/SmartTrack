# SmartTrack – Project Write-up

## 1. Project Overview

SmartTrack is a web application that helps B.Tech students track academic progress and plan future semesters. Instead of relying on spreadsheets, students can record completed courses, monitor basket-wise progress, and plan upcoming semesters through a clear dashboard.

The system is built specifically around IIT Gandhinagar’s curriculum structure, supporting batch-wise graduation requirements, discipline-specific baskets, and IITGN’s grading system.

## 2. Technical Decisions

**Django as the backend framework**  
Django was chosen because it provides built-in authentication, a powerful ORM, and a clear project structure. These features allowed core requirements like user accounts, data management, and secure access to be implemented faster.

**Vanilla HTML and CSS for the frontend**  
HTML and CSS were used instead of a JavaScript framework because of prior knowledge in them. This decision helped me focus on building actual product development with suitable features.

**Multi-page architecture**  
The application uses separate Django-rendered pages(in the main pages) rather than a single-page application that required Javascript. At my present skill level this approach was reliable and I created a mutiple pages with full functionalities without unnecessary complexity.

**Database: SQLite during development, PostgreSQL in production**  
SQLite was used locally for zero-configuration development. Then for deployment in Railway PostgreSQL was adopted for better handling of persistent data(suitable for multiple users).

**Reusable helper functions**  
Credit totals, basket progress percentages, and SPI calculations were extracted into helper functions. This kept the codebase clean and reduced the chance of inconsistent results across different pages.

## 3. Challenges Faced

**1. Frontend was built before backend was planned**  
The frontend was developed before the backend structure was fully finalised. This caused several pages to be restructured when data requirements did not match the original HTML layout. Planning the data flow before building pages would have saved considerable time.

**2. Basket assignment ambiguity**  
Basket tracking was more complex than expected. After studying IITGN’s advisory documents, it became clear that some courses can belong to different baskets depending on a student’s situation.  
**Solution I used in SmartTrack:** Students select the basket themselves when adding a course. This produces more accurate progress statistics.

**3. Duplicate course counting in the semester planner**  
Planned courses that already existed in the completed list were being counted twice, leading to incorrect credit totals.

**4. Deployment issues**  
Moving from local development to production deployment introduced problems with static files, database migration (SQLite → PostgreSQL), ALLOWED_HOSTS, and CSRF verification.

## 4. What I Would Do With More Time

1. **Fully responsive mobile interface**  
   Build a dedicated mobile layout with a collapsible sidebar.

2. **Additional Features**
   Features like Downloading Excel report of course history.

3. **Automated basket assignment**  
   Maintain a complete IITGN course catalog with default basket mappings, while still allowing manual selection for ambiguous cases.

4. Design and structure this App for students of academic years before 2025-26.
5. Make the Authentication stronger.
6. Making the UI more professional.

Demo link: https://canva.link/7g1xrt17r6j2ioe
