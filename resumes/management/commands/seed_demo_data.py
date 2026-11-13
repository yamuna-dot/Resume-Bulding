from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from resumes.models import Resume, Education, Experience, Project, Skill, Certification


class Command(BaseCommand):
    help = "Seeds initial demo users and professional sample resumes."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding demo data...")

        # 1. Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@resumecraft.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin12345')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin / admin12345)"))
        else:
            self.stdout.write("Admin user already exists.")

        # 2. Demo User
        demo_user, created = User.objects.get_or_create(
            username='yamuna',
            defaults={
                'email': 'yamuna@example.com',
                'first_name': 'Yamuna',
                'last_name': 'Devi',
            }
        )
        if created:
            demo_user.set_password('yamuna12345')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS("Created demo user (yamuna / yamuna12345)"))
        else:
            self.stdout.write("Demo user 'yamuna' already exists.")

        # 3. Create Sample Resume 1 (Modern Professional)
        r1, r1_created = Resume.objects.get_or_create(
            user=demo_user,
            title="Full Stack Python & Django Developer",
            defaults={
                'template_choice': 'modern',
                'full_name': 'Yamuna Devi',
                'email': 'yamuna.developer@example.com',
                'phone': '+91 98765 43210',
                'address': 'Hyderabad, Telangana, India',
                'linkedin_url': 'linkedin.com/in/yamunadevi',
                'github_url': 'github.com/yamunadevi',
                'portfolio_url': 'yamunadev.io',
                'summary': (
                    "Results-oriented Full Stack Developer with solid expertise in Python, Django, MySQL, and modern frontend technologies. "
                    "Demonstrated track record of designing responsive web applications, building scalable RESTful APIs, and implementing "
                    "secure database schemas with optimized query performance."
                ),
                'achievements': (
                    "- 1st Prize Winner in National College Web Hackathon 2024 for developing an AI study companion.\n"
                    "- Solved 300+ Data Structures & Algorithms challenges across LeetCode and HackerRank.\n"
                    "- Published technical article on 'Building Scalable Web Backends with Django and MySQL'."
                ),
                'languages': 'English (Fluent), Telugu (Native), Hindi (Conversational)',
                'hobbies': 'Open Source Contributing, Algorithm Puzzles, Tech Blogging, Chess',
            }
        )

        if r1_created:
            # Educations
            Education.objects.create(
                resume=r1,
                degree="Bachelor of Technology in Computer Science & Engineering",
                college_name="JNTU College of Engineering",
                university="Jawaharlal Nehru Technological University",
                graduation_year="2020 - 2024",
                percentage_or_cgpa="8.85 CGPA",
                order=0
            )
            Education.objects.create(
                resume=r1,
                degree="Higher Secondary Certificate (Class XII)",
                college_name="Sri Chaitanya Junior College",
                university="Telangana Board of Intermediate",
                graduation_year="2018 - 2020",
                percentage_or_cgpa="94.6%",
                order=1
            )

            # Experiences
            Experience.objects.create(
                resume=r1,
                company_name="TechMatrix Solutions Pvt Ltd",
                job_role="Software Engineer Intern",
                duration="June 2023 - May 2024",
                responsibilities=(
                    "- Architected and deployed Django backend services handling 15,000+ daily requests.\n"
                    "- Developed custom MySQL stored procedures, indices, and ORM query optimizations reducing latency by 35%.\n"
                    "- Collaborated with frontend engineers to build responsive Bootstrap 5 dashboards and interactive forms."
                ),
                order=0
            )

            # Projects
            Project.objects.create(
                resume=r1,
                title="ResumeCraft - Online Resume Builder",
                technologies_used="Python, Django 5, MySQL 8, HTML5, CSS3, JavaScript, xhtml2pdf",
                description=(
                    "Engineered a full-featured resume management portal with multi-template rendering (Modern, Minimal, Fresher), "
                    "instant PDF generation, secure role-isolated user dashboards, and dynamic multi-item JavaScript forms."
                ),
                project_link="github.com/yamunadevi/resumebuilder",
                order=0
            )
            Project.objects.create(
                resume=r1,
                title="E-Commerce Store & Inventory Manager",
                technologies_used="Django, MySQL, JavaScript, Bootstrap, Stripe API",
                description=(
                    "Built an end-to-end e-commerce store with product cataloging, session-based cart, secure checkout, "
                    "and administrative dashboard for tracking stock and order status."
                ),
                project_link="github.com/yamunadevi/onlineshop",
                order=1
            )

            # Skills
            skills_data = [
                ('Python', 'programming', 'Expert'),
                ('JavaScript', 'programming', 'Advanced'),
                ('C++', 'programming', 'Intermediate'),
                ('MySQL', 'database', 'Expert'),
                ('PostgreSQL', 'database', 'Advanced'),
                ('Django Framework', 'web', 'Expert'),
                ('HTML5 & CSS3', 'web', 'Expert'),
                ('Bootstrap 5', 'web', 'Expert'),
                ('Git & GitHub', 'other', 'Advanced'),
                ('RESTful APIs', 'other', 'Advanced'),
            ]
            for idx, (name, cat, prof) in enumerate(skills_data):
                Skill.objects.create(resume=r1, name=name, category=cat, proficiency=prof, order=idx)

            # Certifications
            Certification.objects.create(
                resume=r1,
                name="Meta Backend Developer Professional Certificate",
                issuing_organization="Coursera / Meta",
                issue_year="2024",
                order=0
            )
            Certification.objects.create(
                resume=r1,
                name="Python for Data Science and Web Development",
                issuing_organization="HackerRank",
                issue_year="2023",
                order=1
            )
            self.stdout.write(self.style.SUCCESS("Created sample resume 'Full Stack Python & Django Developer'"))

        # 4. Create Sample Resume 2 (Fresher / Student Template)
        r2, r2_created = Resume.objects.get_or_create(
            user=demo_user,
            title="Fresher Graduate Software Developer",
            defaults={
                'template_choice': 'fresher',
                'full_name': 'Yamuna Devi',
                'email': 'yamuna.devi@example.com',
                'phone': '+91 98765 43210',
                'address': 'Hyderabad, India',
                'linkedin_url': 'linkedin.com/in/yamunadevi',
                'github_url': 'github.com/yamunadevi',
                'summary': (
                    "Motivated Computer Science graduate eager to apply strong programming foundations, database design skills, "
                    "and passion for scalable web development in an entry-level Software Engineer role."
                ),
                'achievements': (
                    "- Winner of University TechFest Coding Competition 2023.\n"
                    "- Completed 6-month intensive web development training program."
                ),
                'languages': 'English, Telugu, Hindi',
                'hobbies': 'Competitive Coding, Reading Tech News, Badminton',
            }
        )

        if r2_created:
            Education.objects.create(
                resume=r2,
                degree="B.Tech Computer Science & Engineering",
                college_name="Engineering College of Technology",
                university="JNTU Hyderabad",
                graduation_year="2024",
                percentage_or_cgpa="8.9 CGPA",
                order=0
            )
            Skill.objects.create(resume=r2, name="Python", category="programming", proficiency="Advanced", order=0)
            Skill.objects.create(resume=r2, name="Java", category="programming", proficiency="Intermediate", order=1)
            Skill.objects.create(resume=r2, name="MySQL", category="database", proficiency="Advanced", order=2)
            Skill.objects.create(resume=r2, name="Django & HTML/CSS", category="web", proficiency="Advanced", order=3)

            Project.objects.create(
                resume=r2,
                title="Student Academic Record Management System",
                technologies_used="Python, Django, MySQL",
                description="Designed a database-backed portal for managing student attendance, grades, and report card generation.",
                order=0
            )

            Certification.objects.create(
                resume=r2,
                name="Python Certified Associate Programmer",
                issuing_organization="Python Institute",
                issue_year="2023",
                order=0
            )
            self.stdout.write(self.style.SUCCESS("Created sample resume 'Fresher Graduate Software Developer'"))

        self.stdout.write(self.style.SUCCESS("Successfully seeded demo data!"))
