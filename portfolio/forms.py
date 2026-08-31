from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class RegisterForm(UserCreationForm):
    email         = forms.EmailField(required=True)
    username_slug = forms.SlugField(
        required=True,
        help_text="Your public URL: portfolio.com/YOUR_SLUG (only letters, numbers, hyphens)"
    )

    class Meta:
        model  = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username_slug(self):
        slug = self.cleaned_data['username_slug'].lower()
        if UserProfile.objects.filter(username_slug=slug).exists():
            raise forms.ValidationError("This URL slug is already taken.")
        reserved = ['admin', 'login', 'logout', 'register', 'dashboard', 'static', 'media']
        if slug in reserved:
            raise forms.ValidationError("This slug is reserved. Please choose another.")
        return slug


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model   = PersonalInfo
        exclude = ['user', 'update_at']   
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 6}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model   = Project
        exclude = ['user', 'id', 'slug', 'created_at', 'updated_at', 'order']   # ← added order


class ExperienceForm(forms.ModelForm):
    class Meta:
        model   = Experience
        exclude = ['user', 'order']   # ← added order
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model   = Education
        exclude = ['user', 'order']   # ← added order
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'type': 'date'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model   = Skill
        exclude = ['user', 'order']   # ← added order


class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model   = SkillCategory
        exclude = ['user', 'order']   # ← added order


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model   = SocialLink
        exclude = ['user', 'order']   # ← added order