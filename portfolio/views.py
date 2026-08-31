from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse

from .models import (
    UserProfile, PersonalInfo, SocialLink, Project, Experience,
    Education, SkillCategory, Skill, Tag, ContactMessage,
)
from .forms import (
    RegisterForm, PersonalInfoForm, ProjectForm, ExperienceForm,
    EducationForm, SkillForm, SkillCategoryForm, SocialLinkForm,
)


# ════════════════════════════════════════════════════════════════════
# LANDING
# ════════════════════════════════════════════════════════════════════

def landing(request):
    """
    Root page. If the visitor is logged in, send them straight to their
    dashboard. Otherwise show a simple marketing/landing page that lets
    people register, log in, or jump to a known portfolio URL.
    """
    if request.user.is_authenticated:
        return redirect('public_portfolio', username=request.user.profile.username_slug)
    return render(request, 'website/landing.html')


# ════════════════════════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════════════════════════
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # signals.py already created UserProfile + PersonalInfo with a
            # default slug equal to the username — overwrite with the slug
            # the person actually chose on the register form.
            profile = user.profile
            profile.username_slug = form.cleaned_data['username_slug']
            profile.save()

            login(request, user)
            messages.success(request, "Welcome! Let's set up your portfolio.")
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url or 'dashboard')
        messages.error(request, 'Invalid username or password.')

    next_url = request.GET.get('next', '')
    return render(request, 'auth/login.html', {'next': next_url})


def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('login')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — OVERVIEW
# ════════════════════════════════════════════════════════════════════
@login_required
def dashboard(request):
    user = request.user
    profile = user.profile
    info = PersonalInfo.objects.filter(user=user).first()

    context = {
        'profile':      profile,
        'info':         info,
        'project_count':    Project.objects.filter(user=user).count(),
        'experience_count': Experience.objects.filter(user=user).count(),
        'education_count':  Education.objects.filter(user=user).count(),
        'skill_count':      Skill.objects.filter(user=user).count(),
        'message_count':    ContactMessage.objects.filter(portfolio_owner=user, status='new').count(),
        'portfolio_url':    request.build_absolute_uri(f'/{profile.username_slug}/'),
        'active_nav':       'overview',
    }
    return render(request, 'dashboard/overview.html', context)


@login_required
def toggle_publish(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.is_published = not profile.is_published
        profile.save()
        if profile.is_published:
            messages.success(request, 'Your portfolio is now live! 🎉')
        else:
            messages.info(request, 'Your portfolio is now private.')
    return redirect('dashboard')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — PERSONAL INFO
# ════════════════════════════════════════════════════════════════════
@login_required
def edit_personal(request):
    info, _ = PersonalInfo.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, 'Personal info updated.')
            return redirect('edit_personal')
    else:
        form = PersonalInfoForm(instance=info)

    return render(request, 'dashboard/personal.html', {'form': form, 'info': info, 'active_nav': 'personal'})


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — PROJECTS
# ════════════════════════════════════════════════════════════════════
@login_required
def manage_projects(request):
    projects = Project.objects.filter(user=request.user).order_by('order', '-created_at')
    return render(request, 'dashboard/projects.html', {'projects': projects, 'active_nav': 'projects'})


@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            form.save_m2m()
            messages.success(request, 'Project added.')
            return redirect('manage_projects')
    else:
        form = ProjectForm()

    return render(request, 'dashboard/project_form.html', {'form': form, 'mode': 'add', 'active_nav': 'projects'})


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated.')
            return redirect('manage_projects')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'dashboard/project_form.html', {'form': form, 'mode': 'edit', 'project': project, 'active_nav': 'projects'})


@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted.')
    return redirect('manage_projects')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — EXPERIENCE
# ════════════════════════════════════════════════════════════════════
@login_required
def manage_experience(request):
    experiences = Experience.objects.filter(user=request.user).order_by('order', '-start_date')
    edit_id = request.GET.get('edit')
    instance = get_object_or_404(Experience, pk=edit_id, user=request.user) if edit_id else None

    if request.method == 'POST':
        instance = get_object_or_404(Experience, pk=request.POST.get('pk'), user=request.user) if request.POST.get('pk') else None
        form = ExperienceForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.save()
            messages.success(request, 'Experience saved.')
            return redirect('manage_experience')
    else:
        form = ExperienceForm(instance=instance)

    return render(request, 'dashboard/experience.html', {
        'experiences': experiences, 'form': form, 'editing': instance, 'active_nav': 'experience',
    })


@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience removed.')
    return redirect('manage_experience')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — EDUCATION
# ════════════════════════════════════════════════════════════════════
@login_required
def manage_education(request):
    educations = Education.objects.filter(user=request.user).order_by('order', '-start_date')
    edit_id = request.GET.get('edit')
    instance = get_object_or_404(Education, pk=edit_id, user=request.user) if edit_id else None

    if request.method == 'POST':
        instance = get_object_or_404(Education, pk=request.POST.get('pk'), user=request.user) if request.POST.get('pk') else None
        form = EducationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.user = request.user
            edu.save()
            messages.success(request, 'Education saved.')
            return redirect('manage_education')
    else:
        form = EducationForm(instance=instance)

    return render(request, 'dashboard/education.html', {
        'educations': educations, 'form': form, 'editing': instance, 'active_nav': 'education',
    })


@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, user=request.user)
    if request.method == 'POST':
        edu.delete()
        messages.success(request, 'Education entry removed.')
    return redirect('manage_education')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — SKILLS
# ════════════════════════════════════════════════════════════════════
@login_required
def manage_skills(request):
    categories = SkillCategory.objects.filter(user=request.user).prefetch_related('skills').order_by('order')
    uncategorized = Skill.objects.filter(user=request.user, category__isnull=True).order_by('order')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'category':
            cat_form = SkillCategoryForm(request.POST)
            if cat_form.is_valid():
                cat = cat_form.save(commit=False)
                cat.user = request.user
                cat.save()
                messages.success(request, 'Category added.')
                return redirect('manage_skills')

        elif form_type == 'skill':
            skill_form = SkillForm(request.POST, request.FILES)
            # Restrict category choices to this user's categories
            skill_form.fields['category'].queryset = SkillCategory.objects.filter(user=request.user)
            if skill_form.is_valid():
                skill = skill_form.save(commit=False)
                skill.user = request.user
                skill.save()
                messages.success(request, 'Skill added.')
                return redirect('manage_skills')
    else:
        skill_form = SkillForm()
        skill_form.fields['category'].queryset = SkillCategory.objects.filter(user=request.user)
        cat_form = SkillCategoryForm()

    return render(request, 'dashboard/skills.html', {
        'categories': categories,
        'uncategorized': uncategorized,
        'skill_form': skill_form,
        'cat_form': cat_form,
        'active_nav': 'skills',
    })


@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill removed.')
    return redirect('manage_skills')


@login_required
def delete_skill_category(request, pk):
    cat = get_object_or_404(SkillCategory, pk=pk, user=request.user)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category removed.')
    return redirect('manage_skills')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — SOCIAL LINKS
# ════════════════════════════════════════════════════════════════════
@login_required
def manage_social(request):
    links = SocialLink.objects.filter(user=request.user).order_by('order')

    if request.method == 'POST':
        form = SocialLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            messages.success(request, 'Social link added.')
            return redirect('manage_social')
    else:
        form = SocialLinkForm()

    return render(request, 'dashboard/social.html', {'links': links, 'form': form, 'active_nav': 'social'})


@login_required
def delete_social(request, pk):
    link = get_object_or_404(SocialLink, pk=pk, user=request.user)
    if request.method == 'POST':
        link.delete()
        messages.success(request, 'Social link removed.')
    return redirect('manage_social')


# ════════════════════════════════════════════════════════════════════
# DASHBOARD — MESSAGES
# ════════════════════════════════════════════════════════════════════
@login_required
def view_messages(request):
    inbox = ContactMessage.objects.filter(portfolio_owner=request.user).order_by('-created_at')

    if request.method == 'POST':
        msg_id = request.POST.get('mark_read')
        if msg_id:
            ContactMessage.objects.filter(pk=msg_id, portfolio_owner=request.user).update(status='read')
            return redirect('view_messages')

    return render(request, 'dashboard/messages.html', {'inbox': inbox, 'active_nav': 'messages'})


# ════════════════════════════════════════════════════════════════════
# PUBLIC PORTFOLIO (no login needed)
# ════════════════════════════════════════════════════════════════════
def public_portfolio(request, username):
    try:
        profile = UserProfile.objects.get(username_slug=username)
    except UserProfile.DoesNotExist:
        # Friendly 404 — not Django's default error page
        return render(request, 'website/not_found.html', {'username': username}, status=404)
    user = profile.user
    is_owner = request.user.is_authenticated and request.user == user

    # Owners can always preview their own (unpublished) portfolio.
    if not profile.is_published and not is_owner:
        return render(request, 'website/coming_soon.html', {'profile': profile}, status=404)

    

    # Handle contact form submissions
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ip = request.META.get('REMOTE_ADDR')
            ContactMessage.objects.create(
                portfolio_owner=user,
                name=name, email=email,
                subject=subject, message=message,
                ip_address=ip,
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok'})
            messages.success(request, "Message sent! I'll get back to you soon.")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error'}, status=400)

    context = {
        'profile':          profile,
        'is_owner':         is_owner,
        'portfolio_page':   True,
        'info':             PersonalInfo.objects.filter(user=user).first(),
        'social_links':     SocialLink.objects.filter(user=user, is_active=True).order_by('order'),
        'projects':         Project.objects.filter(user=user, status='published').order_by('order'),
        'experiences':      Experience.objects.filter(user=user).order_by('order', '-start_date'),
        'education':        Education.objects.filter(user=user).order_by('order', '-start_date'),
        'skill_categories': SkillCategory.objects.filter(user=user).prefetch_related('skills').order_by('order'),
        'skills':           Skill.objects.filter(user=user).order_by('category__order', 'order'),
        'featured_skills':  Skill.objects.filter(user=user, is_featured=True).order_by('order'),
        'portfolio_user':   user,
    }
    return render(request, 'website/portfolio.html', context)