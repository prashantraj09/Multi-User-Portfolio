from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import uuid


# ── User Profile (extends Django's User) ──────────────────────────
class UserProfile(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username_slug = models.SlugField(max_length=50, unique=True, help_text="Your public URL: portfolio.com/YOUR_SLUG")
    is_published  = models.BooleanField(default=False, help_text="Make portfolio publicly visible")
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.username_slug}"


# ── Personal Info (one per user) ──────────────────────────────────
class PersonalInfo(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_info')
    full_name      = models.CharField(max_length=60)
    tagline        = models.CharField(max_length=200)
    bio            = models.TextField()
    profile_image  = models.ImageField(upload_to='portfolio/profile/', blank=True, null=True)
    resume_file    = models.FileField(upload_to='portfolio/resume/', blank=True, null=True)
    email          = models.EmailField()
    phone          = models.CharField(max_length=20, blank=True)
    location       = models.CharField(max_length=200, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    open_to_work   = models.BooleanField(default=True)
    update_at     = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


# ── Social Links ───────────────────────────────────────────────────
class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('github', 'GitHub'), ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter / X'), ('instagram', 'Instagram'),
        ('website', 'Personal Website'), ('other', 'Other'),
    ]
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_links')
    platform  = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url       = models.URLField()
    label     = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)
    order     = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} — {self.platform}"


# ── Projects ───────────────────────────────────────────────────────
class Project(models.Model):
    STATUS_CHOICES = [('draft','Draft'),('published','Published'),('archived','Archived')]
    TYPE_CHOICES   = [
        ('web','Web App'),('mobile','Mobile App'),('desktop','Desktop App'),
        ('api','API / Backend'),('ml','Machine Learning'),
        ('design','UI/UX Design'),('open_source','Open Source'),('other','Other'),
    ]
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    id            = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title         = models.CharField(max_length=120)
    slug          = models.SlugField(max_length=140, blank=True)
    subtitle      = models.CharField(max_length=200, blank=True)
    description   = models.TextField()
    project_type  = models.CharField(max_length=20, choices=TYPE_CHOICES, default='web')
    tags          = models.ManyToManyField('Tag', blank=True, related_name='projects')
    thumbnail     = models.ImageField(upload_to='portfolio/projects/thumbnails/', blank=True, null=True)
    cover_image   = models.ImageField(upload_to='portfolio/projects/covers/', blank=True, null=True)
    live_url      = models.URLField(blank=True)
    repo_url      = models.URLField(blank=True)
    case_study_url = models.URLField(blank=True)
    technologies  = models.CharField(max_length=500, blank=True)
    status        = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft')
    is_featured   = models.BooleanField(default=False)
    start_date    = models.DateField(blank=True, null=True)
    end_date      = models.DateField(blank=True, null=True)
    order         = models.PositiveSmallIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} — {self.title}"


# ── Experience ─────────────────────────────────────────────────────
class Experience(models.Model):
    EMPLOYMENT_TYPE = [
        ('full_time','Full-time'),('part_time','Part-time'),
        ('contract','Contract'),('freelance','Freelance'),
        ('internship','Internship'),('volunteer','Volunteer'),
    ]
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company         = models.CharField(max_length=120)
    company_logo    = models.ImageField(upload_to='portfolio/experience/', blank=True, null=True)
    company_url     = models.URLField(blank=True)
    role            = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE, default='full_time')
    location        = models.CharField(max_length=100, blank=True)
    is_remote       = models.BooleanField(default=False)
    description     = models.TextField(blank=True)
    technologies    = models.CharField(max_length=500, blank=True)
    start_date      = models.DateField()
    end_date        = models.DateField(blank=True, null=True)
    order           = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} — {self.role} @ {self.company}"


# ── Education ──────────────────────────────────────────────────────
class Education(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    institution      = models.CharField(max_length=150)
    institution_logo = models.ImageField(upload_to='portfolio/education/', blank=True, null=True)
    degree           = models.CharField(max_length=100)
    field_of_study   = models.CharField(max_length=100, blank=True)
    description      = models.TextField(blank=True)
    grade            = models.CharField(max_length=20, blank=True)
    start_date       = models.DateField()
    end_date         = models.DateField(blank=True, null=True)
    order            = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} — {self.degree}"


# ── Skills ─────────────────────────────────────────────────────────
class SkillCategory(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_categories')
    name  = models.CharField(max_length=60)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} — {self.name}"


class Skill(models.Model):
    LEVEL_CHOICES = [(1,'Beginner'),(2,'Elementary'),(3,'Intermediate'),(4,'Advanced'),(5,'Expert')]
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    category    = models.ForeignKey(SkillCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='skills')
    name        = models.CharField(max_length=60)
    icon        = models.ImageField(upload_to='portfolio/skills/', blank=True, null=True)
    icon_class  = models.CharField(max_length=60, blank=True)
    proficiency = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=3)
    is_featured = models.BooleanField(default=False)
    order       = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} — {self.name}"


# ── Tags (global, not per user) ────────────────────────────────────
class Tag(models.Model):
    name  = models.CharField(max_length=50, unique=True)
    slug  = models.SlugField(max_length=60, unique=True, blank=True)
    color = models.CharField(max_length=7, default='#6366f1')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ── Contact Messages ───────────────────────────────────────────────
class ContactMessage(models.Model):
    STATUS_CHOICES = [('new','New'),('read','Read'),('replied','Replied'),('archived','Archived')]
    portfolio_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    name       = models.CharField(max_length=100)
    email      = models.EmailField()
    subject    = models.CharField(max_length=200, blank=True)
    message    = models.TextField()
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.portfolio_owner.username} | From: {self.name}"