from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from resumes.models import Resume, Education, Experience, Project, Skill, Certification


class ResumesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password123', email='u1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password123', email='u2@example.com')
        
        self.resume1 = Resume.objects.create(
            user=self.user1,
            title='Python Full Stack Resume',
            template_choice='modern',
            full_name='Alice Smith',
            email='alice@example.com',
            phone='+1 555-1234',
            address='New York, NY',
            summary='Experienced Python Developer with strong Django and MySQL skills.',
            languages='English, Spanish',
            hobbies='Chess, Open Source',
            achievements='Dean List 2023\nHackathon Winner'
        )

        Education.objects.create(
            resume=self.resume1,
            degree='B.Tech in Computer Science',
            college_name='NYIT',
            university='State University',
            graduation_year='2020 - 2024',
            percentage_or_cgpa='3.9 GPA'
        )

        Skill.objects.create(
            resume=self.resume1,
            name='Python',
            category='programming',
            proficiency='Expert'
        )

        Skill.objects.create(
            resume=self.resume1,
            name='MySQL',
            category='database',
            proficiency='Advanced'
        )

        Project.objects.create(
            resume=self.resume1,
            title='E-Commerce Platform',
            technologies_used='Django, MySQL, Bootstrap',
            description='Built full scalable e-commerce site with payment integration.'
        )

    def test_dashboard_access_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_authenticated(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Full Stack Resume')
        self.assertContains(response, 'Alice Smith')

    def test_user_isolation(self):
        # User 2 logs in and should NOT see User 1's resume
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Python Full Stack Resume')

        # User 2 tries to preview User 1's resume -> 404
        preview_response = self.client.get(reverse('resume_preview', args=[self.resume1.pk]))
        self.assertEqual(preview_response.status_code, 404)

        # User 2 tries to edit User 1's resume -> 404
        edit_response = self.client.get(reverse('resume_edit', args=[self.resume1.pk]))
        self.assertEqual(edit_response.status_code, 404)

    def test_resume_preview_templates(self):
        self.client.login(username='user1', password='password123')

        # Modern template
        r1 = self.client.get(reverse('resume_preview', args=[self.resume1.pk]) + '?template=modern')
        self.assertEqual(r1.status_code, 200)
        self.assertContains(r1, 'tmpl-modern')

        # Minimal template
        r2 = self.client.get(reverse('resume_preview', args=[self.resume1.pk]) + '?template=minimal')
        self.assertEqual(r2.status_code, 200)
        self.assertContains(r2, 'tmpl-minimal')

        # Fresher template
        r3 = self.client.get(reverse('resume_preview', args=[self.resume1.pk]) + '?template=fresher')
        self.assertEqual(r3.status_code, 200)
        self.assertContains(r3, 'tmpl-fresher')

    def test_resume_pdf_download(self):
        self.client.login(username='user1', password='password123')
        pdf_url = reverse('resume_pdf', args=[self.resume1.pk])
        response = self.client.get(pdf_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(len(response.content) > 500)

    def test_resume_create_and_delete(self):
        self.client.login(username='user1', password='password123')
        create_data = {
            'title': 'New Test Resume',
            'template_choice': 'fresher',
            'full_name': 'Bob Tester',
            'email': 'bob@example.com',
            'phone': '1234567890',
            'address': 'Test City',
            'summary': 'Passionate Fresher ready for challenges',
            'education_degree[]': ['B.Sc IT'],
            'education_college[]': ['City College'],
            'education_university[]': ['City Uni'],
            'education_year[]': ['2024'],
            'education_score[]': ['85%'],
            'skill_name[]': ['Python', 'SQL'],
            'skill_category[]': ['programming', 'database'],
            'skill_proficiency[]': ['Intermediate', 'Beginner'],
        }
        res = self.client.post(reverse('resume_create'), create_data)
        self.assertEqual(res.status_code, 302)
        new_resume = Resume.objects.filter(title='New Test Resume').first()
        self.assertIsNotNone(new_resume)
        self.assertEqual(new_resume.educations.count(), 1)
        self.assertEqual(new_resume.skills.count(), 2)

        # Delete resume
        del_res = self.client.post(reverse('resume_delete', args=[new_resume.pk]))
        self.assertEqual(del_res.status_code, 302)
        self.assertFalse(Resume.objects.filter(title='New Test Resume').exists())
