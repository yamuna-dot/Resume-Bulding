from django.contrib import admin
from .models import Resume, Education, Experience, Project, Skill, Certification


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'full_name', 'user', 'template_choice', 'updated_at')
    list_filter = ('template_choice', 'created_at', 'updated_at')
    search_fields = ('title', 'full_name', 'email', 'user__username')
    inlines = [EducationInline, ExperienceInline, ProjectInline, SkillInline, CertificationInline]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'college_name', 'resume', 'graduation_year')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_role', 'company_name', 'resume', 'duration')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technologies_used', 'resume')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'resume')
    list_filter = ('category', 'proficiency')


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuing_organization', 'issue_year', 'resume')
