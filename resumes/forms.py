from django import forms
from .models import Resume


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title',
            'template_choice',
            'full_name',
            'email',
            'phone',
            'address',
            'profile_picture',
            'linkedin_url',
            'github_url',
            'portfolio_url',
            'summary',
            'achievements',
            'languages',
            'hobbies',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Senior Software Engineer Resume'
            }),
            'template_choice': forms.Select(attrs={
                'class': 'form-select'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 000-0000 or +91 98765 43210'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, State, Country'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'linkedin_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'github_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username'
            }),
            'portfolio_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://yourwebsite.com'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a compelling career objective or professional summary highlighting your key strengths and goals...'
            }),
            'achievements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your top achievements (one per line, e.g.:\n- Winner of National Hackathon 2024\n- Published research paper on ML in IEEE)'
            }),
            'languages': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. English (Fluent), Telugu (Native), Hindi (Conversational)'
            }),
            'hobbies': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Open Source Contribution, Photography, Chess, Tech Blogging'
            }),
        }
