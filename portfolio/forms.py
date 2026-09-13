from django import forms
from django.contrib.auth.models import User
from .models import (
    UserProfile, PersonalInfo, Project,
    Experience, Education, Skill,
    SkillCategory, SocialLink,
)


# ══════════════════════════════════════════════════════════════════
#  REGISTER — one username field only
# ══════════════════════════════════════════════════════════════════

class RegisterForm(forms.Form):
    """
    Registration form with:
      • full_name  — display name shown on portfolio
      • username   — unique slug used for login AND public URL
      • email
      • password / confirm
    """
    full_name = forms.CharField(
        max_length=60,
        help_text="Your display name shown on your portfolio (e.g. Prashant Raj)",
    )
    username = forms.SlugField(
        max_length=50,
        help_text="Unique ID used to login and as your public URL — only letters, numbers, hyphens",
    )
    email     = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        min_length=8,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        username = self.cleaned_data['username'].lower().strip()

        # Reserved words that would clash with URL patterns
        reserved = [
            'admin', 'login', 'logout', 'register', 'dashboard',
            'static', 'media', 'test-upload', 'api', 'about',
            'contact', 'help', 'support', 'home', 'index',
        ]
        if username in reserved:
            raise forms.ValidationError(
                f'"{username}" is a reserved word. Please choose a different username.'
            )

        # Must be unique in both User.username and UserProfile.username_slug
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken. Please choose another.'
            )
        if UserProfile.objects.filter(username_slug=username).exists():
            raise forms.ValidationError(
                'This username is already taken. Please choose another.'
            )
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'An account with this email already exists.'
            )
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Passwords don't match.")
        return cleaned

    def save(self):
        """Create User + UserProfile + PersonalInfo and return the user."""
        username  = self.cleaned_data['username']
        full_name = self.cleaned_data['full_name'].strip()
        email     = self.cleaned_data['email']
        password  = self.cleaned_data['password1']

        # Split full name into first/last for Django's User model
        parts      = full_name.split(' ', 1)
        first_name = parts[0]
        last_name  = parts[1] if len(parts) > 1 else ''

        # Create Django user — username IS the slug
        user = User.objects.create_user(
            username   = username,
            email      = email,
            password   = password,
            first_name = first_name,
            last_name  = last_name,
        )

        # UserProfile (signal may already create one; get_or_create is safe)
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.username_slug = username
        profile.save()

        # PersonalInfo seeded with name + email
        PersonalInfo.objects.update_or_create(
            user=user,
            defaults={
                'full_name': full_name,
                'email':     email,
                'tagline':   '',
                'bio':       '',
            },
        )

        return user


# ══════════════════════════════════════════════════════════════════
#  DASHBOARD FORMS
# ══════════════════════════════════════════════════════════════════

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model   = PersonalInfo
        exclude = ['user', 'updated_at']
        widgets = {
            'bio':      forms.Textarea(attrs={'rows': 6}),
            'tagline':  forms.TextInput(),
            'location': forms.TextInput(),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model   = Project
        exclude = ['user', 'id', 'slug', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date':  forms.DateInput(attrs={'type': 'date'}),
            'end_date':    forms.DateInput(attrs={'type': 'date'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model   = Experience
        exclude = ['user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date':  forms.DateInput(attrs={'type': 'date'}),
            'end_date':    forms.DateInput(attrs={'type': 'date'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model   = Education
        exclude = ['user']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_date':  forms.DateInput(attrs={'type': 'date'}),
            'end_date':    forms.DateInput(attrs={'type': 'date'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model   = Skill
        exclude = ['user']


class SkillCategoryForm(forms.ModelForm):
    class Meta:
        model   = SkillCategory
        exclude = ['user']


class SocialLinkForm(forms.ModelForm):
    class Meta:
        model   = SocialLink
        exclude = ['user']