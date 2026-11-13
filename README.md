# ResumeCraft - Professional Resume Builder Web Application

A full-featured, responsive, and secure **Resume Builder Web Application** built with **Python Django**, **HTML5**, **CSS3**, **JavaScript**, and **MySQL**.

---

## 1. Project Overview
ResumeCraft is designed for students, fresh graduates, and experienced professionals to create, manage, preview, and export high-quality resumes. The application incorporates Django's built-in authentication system with complete user data isolation, dynamic multi-section resume forms, live A4 preview with instant template switching, and pixel-perfect PDF downloads.

---

## 2. Technology Stack
- **Backend Framework**: Python 3.14 & Django 5.2
- **Database**: MySQL 8.0 (via `mysqlclient`)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3, Font Awesome 6
- **PDF Generation**: `xhtml2pdf` + Browser Print CSS (Dual-Engine export)
- **Authentication**: Django Built-in Authentication (`django.contrib.auth`)

---

## 3. Project Architecture & Folder Structure

```
resumebilding/
│
├── manage.py                          # Django management script
├── README.md                          # Comprehensive documentation
│
├── resumebuilder/                     # Project configuration
│   ├── __init__.py
│   ├── settings.py                    # MySQL DB, media, static, installed apps
│   ├── urls.py                        # Root URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                          # User Authentication App
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                       # Registration & Login forms with validation
│   ├── models.py
│   ├── tests.py                       # Unit tests for auth flows
│   ├── urls.py                        # /accounts/register/, /login/, /logout/
│   └── views.py                       # Register, login, logout view logic
│
├── resumes/                           # Resume Management App
│   ├── admin.py                       # Django Admin with inlines
│   ├── apps.py
│   ├── forms.py                       # Resume form with widgets & styling
│   ├── models.py                      # Resume, Education, Experience, Project, Skill, Certification
│   ├── tests.py                       # Full test suite (CRUD, templates, isolation, PDF)
│   ├── urls.py                        # /resumes/ (dashboard, create, edit, delete, preview, pdf)
│   ├── utils.py                       # PDF rendering engine & system path callback
│   ├── views.py                       # Resume views with atomic child saving
│   └── management/
│       └── commands/
│           └── seed_demo_data.py      # Demo seed script for users and resumes
│
├── templates/                         # HTML Templates
│   ├── base.html                      # Layout: navbar, messages, footer
│   ├── landing.html                   # Platform landing & feature showcase
│   ├── accounts/
│   │   ├── login.html                 # Login page
│   │   └── register.html              # Registration page
│   ├── resumes/
│   │   ├── dashboard.html             # User dashboard with resume cards & stats
│   │   ├── resume_form.html           # Multi-section dynamic creation/editing form
│   │   ├── resume_preview.html        # A4 interactive preview with template switcher
│   │   └── resume_confirm_delete.html # Confirmation modal for safe deletion
│   └── templates_layout/              # Standalone template layouts
│       ├── modern.html                # Modern Professional (Web preview)
│       ├── modern_pdf.html            # Modern Professional (PDF render)
│       ├── minimal.html               # Simple & Minimal (Web preview)
│       ├── minimal_pdf.html           # Simple & Minimal (PDF render)
│       ├── fresher.html               # Fresher / Student (Web preview)
│       └── fresher_pdf.html           # Fresher / Student (PDF render)
│
├── static/                            # Static Assets
│   ├── css/
│   │   ├── style.css                  # Custom theme, blue & light-grey palette
│   │   └── resume_templates.css       # A4 container dimensions & print rules
│   ├── js/
│   │   ├── main.js                    # Flash message dismiss, tooltips
│   │   └── resume_form.js             # Dynamic row add/delete, avatar preview
│   └── images/
│       └── avatar.svg                 # Default user avatar placeholder
│
└── media/                             # Uploaded media (profile pictures)
    └── profile_pics/
```

---

## 4. Database Schema (MySQL)

All tables are created in the MySQL database: `resume_builder_db`.

- **auth_user**: Django user table storing usernames, hashed passwords, emails, and names.
- **resumes_resume**: Stores personal details, summary, achievements, languages, hobbies, links, selected template, and user foreign key (`ON DELETE CASCADE`).
- **resumes_education**: Stores degrees, college names, universities, passing years, and percentages/CGPAs (`ON DELETE CASCADE`).
- **resumes_experience**: Stores companies, roles, durations, and bulleted responsibilities (`ON DELETE CASCADE`).
- **resumes_project**: Stores project titles, tech stacks, descriptions, and links (`ON DELETE CASCADE`).
- **resumes_skill**: Stores skills categorized into *Programming Languages*, *Database Technologies*, *Web Technologies*, and *Other Skills* with proficiency levels (`ON DELETE CASCADE`).
- **resumes_certification**: Stores certificate names, issuing bodies, years, and verification links (`ON DELETE CASCADE`).

---

## 5. Main Features

### A. Authentication & Security
- Secure registration with password length checks, email uniqueness, and password confirmation.
- Secure login and session management.
- Complete data isolation: Users can **only** view, edit, download, and delete their own resumes (`get_object_or_404(Resume, pk=pk, user=request.user)`).

### B. User Dashboard
- Welcome greeting with user's name.
- Summary cards: Total Resumes Created, Available Templates, PDF Ready status.
- Responsive grid of resume cards displaying template badges, timestamps, and quick action buttons.
- Create New Resume button and empty-state guidance.

### C. Resume Creation Form (10 Comprehensive Sections)
1. **Resume Info & Template**: Friendly title and template picker.
2. **Personal Information**: Full name, email, phone, location, profile picture with live image preview, LinkedIn, GitHub, and Portfolio URLs.
3. **Career Objective / Professional Summary**: Formatted summary text.
4. **Education**: Dynamic `+ Add Education` cards with Degree, College, University, Year, and CGPA/Percentage.
5. **Technical Skills**: Dynamic `+ Add Skill` rows with Category and Proficiency dropdowns.
6. **Work Experience / Internships**: Dynamic `+ Add Experience` cards with Company, Role, Duration, and Responsibilities.
7. **Projects**: Dynamic `+ Add Project` cards with Title, Tech Stack, Description, and Project Link.
8. **Certifications**: Dynamic `+ Add Certification` cards with Name, Issuing Organization, and Year.
9. **Achievements**: Multi-line achievements.
10. **Languages & Hobbies**: Structured fields for spoken languages and interests.

### D. Resume Templates
1. **Modern Professional**: Two-column layout with a deep navy sidebar, avatar, skill badges, and clean timeline.
2. **Simple and Minimal**: Clean ATS-friendly single-column layout with crisp section dividers and classic typography.
3. **Fresher / Student Resume**: Specially highlighted for college students and entry-level job seekers with an academic qualifications table, categorized technical skills, and capstone project highlights.

### E. Live A4 Preview & PDF Export
- Authentic A4 layout (210mm x 297mm) rendered on-screen with page elevation shadow.
- Interactive template switcher toolbar to toggle between Modern, Minimal, and Fresher views instantly.
- "Set as Default" button to save the active preview choice back to the database.
- **Dual PDF Generation**:
  - **Download PDF**: Server-side PDF compilation using `xhtml2pdf` preserving exact styling.
  - **Print / Save**: Direct browser print styling (`@media print`) configured with `@page { size: A4; margin: 0; }`.

---

## 6. How to Run the Application

### Step 1: Ensure MySQL Service is Running
MySQL Server 8.0 is running on `localhost:3306`.
Database: `resume_builder_db` (User: `root`, Password: `sai1813`).

### Step 2: Apply Migrations (already done)
```powershell
python manage.py migrate
```

### Step 3: Seed Demo Data (already executed)
To populate sample accounts and resumes:
```powershell
python manage.py seed_demo_data
```

### Step 4: Run the Development Server
```powershell
python manage.py runserver
```

Open your browser at:
`http://127.0.0.1:8000/`

---

## 7. Pre-Configured Demo Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Demo User** | `yamuna` | `yamuna12345` | Has 2 pre-built resumes (Modern & Fresher templates) |
| **Superuser (Admin)** | `admin` | `admin12345` | Full access to `/admin/` portal |

You can also click **"Get Started Free"** on the landing page to register your own custom user account anytime.

---

## 8. Automated Test Suite
Run the 10 automated unit tests:
```powershell
python manage.py test
```
All tests verify registration, authentication, CRUD operations, user isolation, template switching, and PDF rendering.
