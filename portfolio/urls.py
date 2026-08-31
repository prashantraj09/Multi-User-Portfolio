"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Root ──────────────────────────────────────────────────────
    path('', views.landing, name='landing'),

    # ── Auth ──────────────────────────────────────────────────────
    path('register/',        views.register_view,  name='register'),
    path('login/',           views.login_view,     name='login'),
    path('logout/',          views.logout_view,    name='logout'),

    # ── Dashboard (manage portfolio) ──────────────────────────────
    path('dashboard/',                    views.dashboard,           name='dashboard'),
    path('dashboard/personal/',           views.edit_personal,       name='edit_personal'),
    path('dashboard/projects/',           views.manage_projects,     name='manage_projects'),
    path('dashboard/projects/add/',       views.add_project,         name='add_project'),
    path('dashboard/projects/<uuid:pk>/edit/',   views.edit_project,  name='edit_project'),
    path('dashboard/projects/<uuid:pk>/delete/', views.delete_project, name='delete_project'),
    path('dashboard/experience/',         views.manage_experience,   name='manage_experience'),
    path('dashboard/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),
    path('dashboard/education/',          views.manage_education,    name='manage_education'),
    path('dashboard/education/<int:pk>/delete/',  views.delete_education,  name='delete_education'),
    path('dashboard/skills/',             views.manage_skills,       name='manage_skills'),
    path('dashboard/skills/<int:pk>/delete/',     views.delete_skill,      name='delete_skill'),
    path('dashboard/skills/category/<int:pk>/delete/', views.delete_skill_category, name='delete_skill_category'),
    path('dashboard/social/',             views.manage_social,       name='manage_social'),
    path('dashboard/social/<int:pk>/delete/',     views.delete_social,     name='delete_social'),
    path('dashboard/messages/',           views.view_messages,       name='view_messages'),
    path('dashboard/publish/',            views.toggle_publish,      name='toggle_publish'),


    # path('website/portfolio.html/', views.portfolio, name='portfolio'),
    
    
    # ── Public portfolio (must be LAST — catches every remaining /<slug>/) ─
    path('<str:username>/', views.public_portfolio, name='public_portfolio'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)