from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils.text import slugify

from .models import Resume, Education, Experience, Project, Skill, Certification
from .forms import ResumeForm
from .utils import render_to_pdf


def home_view(request):
    """Landing page: redirects authenticated users to dashboard, shows landing page for others."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


@login_required
def dashboard_view(request):
    """User dashboard showing stats and their created resumes."""
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    total_resumes = resumes.count()
    context = {
        'resumes': resumes,
        'total_resumes': total_resumes,
    }
    return render(request, 'resumes/dashboard.html', context)


def save_resume_children(resume, post_data):
    """Helper to parse and save child relationships atomically."""
    # Educations
    degrees = post_data.getlist('education_degree[]')
    colleges = post_data.getlist('education_college[]')
    universities = post_data.getlist('education_university[]')
    years = post_data.getlist('education_year[]')
    scores = post_data.getlist('education_score[]')

    resume.educations.all().delete()
    for i in range(len(degrees)):
        deg = degrees[i].strip() if i < len(degrees) else ''
        if deg:
            Education.objects.create(
                resume=resume,
                degree=deg,
                college_name=colleges[i].strip() if i < len(colleges) else '',
                university=universities[i].strip() if i < len(universities) else '',
                graduation_year=years[i].strip() if i < len(years) else '',
                percentage_or_cgpa=scores[i].strip() if i < len(scores) else '',
                order=i
            )

    # Experiences
    companies = post_data.getlist('experience_company[]')
    roles = post_data.getlist('experience_role[]')
    durations = post_data.getlist('experience_duration[]')
    resps = post_data.getlist('experience_responsibilities[]')

    resume.experiences.all().delete()
    for i in range(len(companies)):
        comp = companies[i].strip() if i < len(companies) else ''
        role = roles[i].strip() if i < len(roles) else ''
        if comp or role:
            Experience.objects.create(
                resume=resume,
                company_name=comp,
                job_role=role,
                duration=durations[i].strip() if i < len(durations) else '',
                responsibilities=resps[i].strip() if i < len(resps) else '',
                order=i
            )

    # Projects
    titles = post_data.getlist('project_title[]')
    techs = post_data.getlist('project_tech[]')
    descs = post_data.getlist('project_description[]')
    links = post_data.getlist('project_link[]')

    resume.projects.all().delete()
    for i in range(len(titles)):
        title = titles[i].strip() if i < len(titles) else ''
        if title:
            Project.objects.create(
                resume=resume,
                title=title,
                technologies_used=techs[i].strip() if i < len(techs) else '',
                description=descs[i].strip() if i < len(descs) else '',
                project_link=links[i].strip() if i < len(links) else '',
                order=i
            )

    # Skills
    skill_names = post_data.getlist('skill_name[]')
    skill_cats = post_data.getlist('skill_category[]')
    skill_profs = post_data.getlist('skill_proficiency[]')

    resume.skills.all().delete()
    for i in range(len(skill_names)):
        name = skill_names[i].strip() if i < len(skill_names) else ''
        if name:
            Skill.objects.create(
                resume=resume,
                name=name,
                category=skill_cats[i].strip() if i < len(skill_cats) else 'programming',
                proficiency=skill_profs[i].strip() if i < len(skill_profs) else 'Intermediate',
                order=i
            )

    # Certifications
    cert_names = post_data.getlist('cert_name[]')
    cert_orgs = post_data.getlist('cert_org[]')
    cert_years = post_data.getlist('cert_year[]')
    cert_links = post_data.getlist('cert_link[]')

    resume.certifications.all().delete()
    for i in range(len(cert_names)):
        name = cert_names[i].strip() if i < len(cert_names) else ''
        if name:
            Certification.objects.create(
                resume=resume,
                name=name,
                issuing_organization=cert_orgs[i].strip() if i < len(cert_orgs) else '',
                issue_year=cert_years[i].strip() if i < len(cert_years) else '',
                credential_id_or_url=cert_links[i].strip() if i < len(cert_links) else '',
                order=i
            )


@login_required
def resume_create_view(request):
    """Create a new resume with all dynamic sections."""
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                resume = form.save(commit=False)
                resume.user = request.user
                resume.save()
                save_resume_children(resume, request.POST)

            messages.success(request, f"Resume '{resume.title}' created successfully!")
            return redirect('resume_preview', pk=resume.pk)
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        # Pre-fill user's name & email from account if available
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            'email': request.user.email,
            'template_choice': 'modern',
        }
        form = ResumeForm(initial=initial_data)

    context = {
        'form': form,
        'is_edit': False,
    }
    return render(request, 'resumes/resume_form.html', context)


@login_required
def resume_edit_view(request, pk):
    """Edit an existing resume owned by current user."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        if form.is_valid():
            with transaction.atomic():
                updated_resume = form.save()
                save_resume_children(updated_resume, request.POST)

            messages.success(request, f"Resume '{updated_resume.title}' updated successfully!")
            return redirect('resume_preview', pk=updated_resume.pk)
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = ResumeForm(instance=resume)

    context = {
        'form': form,
        'resume': resume,
        'is_edit': True,
        'educations': resume.educations.all(),
        'experiences': resume.experiences.all(),
        'projects': resume.projects.all(),
        'skills': resume.skills.all(),
        'certifications': resume.certifications.all(),
    }
    return render(request, 'resumes/resume_form.html', context)


@login_required
def resume_preview_view(request, pk):
    """Preview resume in A4 layout with live template switching."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    # Allow query param template switch (e.g. ?template=fresher)
    template_choice = request.GET.get('template', resume.template_choice)
    if template_choice not in ['modern', 'minimal', 'fresher']:
        template_choice = resume.template_choice

    # Optionally persist template if requested
    if request.GET.get('save_template') == '1' and template_choice != resume.template_choice:
        resume.template_choice = template_choice
        resume.save(update_fields=['template_choice'])
        messages.success(request, f"Default template updated to {resume.get_template_choice_display()}!")

    grouped_skills = resume.get_skills_by_category()

    context = {
        'resume': resume,
        'template_choice': template_choice,
        'grouped_skills': grouped_skills,
    }
    return render(request, 'resumes/resume_preview.html', context)


@login_required
def resume_download_pdf_view(request, pk):
    """Generate and download resume as PDF maintaining the exact template format."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    template_choice = request.GET.get('template', resume.template_choice)
    if template_choice not in ['modern', 'minimal', 'fresher']:
        template_choice = resume.template_choice

    template_file = f"templates_layout/{template_choice}_pdf.html"
    grouped_skills = resume.get_skills_by_category()

    filename = f"{slugify(resume.full_name or 'resume')}_{template_choice}.pdf"

    context = {
        'resume': resume,
        'grouped_skills': grouped_skills,
        'pdf_mode': True,
    }
    return render_to_pdf(template_file, context, filename=filename, download=True)


@login_required
def resume_delete_view(request, pk):
    """Delete a resume owned by current user."""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        title = resume.title
        resume.delete()
        messages.success(request, f"Resume '{title}' was deleted successfully.")
        return redirect('dashboard')

    return render(request, 'resumes/resume_confirm_delete.html', {'resume': resume})
