from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('modern', 'Modern Professional'),
        ('minimal', 'Simple & Minimal'),
        ('fresher', 'Fresher / Student Resume'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=150, help_text="A friendly name for this resume (e.g. Python Developer Resume)")
    template_choice = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='modern')

    # Personal Information
    full_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Online Links (Optional)
    linkedin_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="LinkedIn Profile")
    github_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="GitHub Profile")
    portfolio_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Portfolio / Website")

    # Career Objective / Professional Summary
    summary = models.TextField(verbose_name="Career Objective / Professional Summary")

    # Additional Sections
    achievements = models.TextField(blank=True, null=True, help_text="One achievement per line")
    languages = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated e.g. English, Telugu, Hindi")
    hobbies = models.CharField(max_length=255, blank=True, null=True, help_text="Comma-separated e.g. Chess, Reading, Open Source")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.full_name}"

    def get_achievements_list(self):
        if not self.achievements:
            return []
        lines = [line.strip().lstrip('-*• ') for line in self.achievements.splitlines() if line.strip()]
        return lines

    def get_languages_list(self):
        if not self.languages:
            return []
        return [lang.strip() for lang in self.languages.split(',') if lang.strip()]

    def get_hobbies_list(self):
        if not self.hobbies:
            return []
        return [h.strip() for h in self.hobbies.split(',') if h.strip()]

    def get_skills_by_category(self):
        grouped = {
            'programming': [],
            'database': [],
            'web': [],
            'other': [],
        }
        for skill in self.skills.all():
            cat = skill.category if skill.category in grouped else 'other'
            grouped[cat].append(skill)
        return grouped


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=150, help_text="e.g. B.Tech in Computer Science")
    college_name = models.CharField(max_length=200, help_text="e.g. ABC College of Engineering")
    university = models.CharField(max_length=200, help_text="e.g. Jawaharlal Nehru Technological University")
    graduation_year = models.CharField(max_length=40, help_text="e.g. 2020 - 2024")
    percentage_or_cgpa = models.CharField(max_length=50, help_text="e.g. 8.5 CGPA or 82%")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.degree} at {self.college_name}"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=150)
    job_role = models.CharField(max_length=150)
    duration = models.CharField(max_length=60, help_text="e.g. June 2023 - Present")
    responsibilities = models.TextField(help_text="Key responsibilities and highlights, one per line or paragraph")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.job_role} at {self.company_name}"

    def get_responsibilities_list(self):
        if not self.responsibilities:
            return []
        return [r.strip().lstrip('-*• ') for r in self.responsibilities.splitlines() if r.strip()]


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=180)
    technologies_used = models.CharField(max_length=255, help_text="e.g. Python, Django, MySQL, Bootstrap")
    description = models.TextField()
    project_link = models.CharField(max_length=255, blank=True, null=True, help_text="GitHub or Live link")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('database', 'Database Technologies'),
        ('web', 'Web Technologies'),
        ('other', 'Other Technical Skills'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='programming')
    name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
            ('Expert', 'Expert'),
        ],
        default='Intermediate'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=200)
    issuing_organization = models.CharField(max_length=180)
    issue_year = models.CharField(max_length=40, help_text="e.g. 2024")
    credential_id_or_url = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization}"
