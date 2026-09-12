<div align="center">

# 🚀 Multi-User Portfolio Platform

### *Build your developer portfolio once — share it forever.*

[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Cloudinary](https://img.shields.io/badge/Cloudinary-Storage-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**[🌐 Live Demo](https://multi-user-portfolio-nnym.onrender.com)** &nbsp;|&nbsp; **[📖 Documentation](#-table-of-contents)** &nbsp;|&nbsp; **[🐛 Report a Bug](https://github.com/prashantraj09/Multi-User-Portfolio/issues)**

<br/>

</div>

---

## 📋 Table of Contents

- [🎯 Motive & Vision](#-motive--vision)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚡ Quick Start (Local Development)](#-quick-start-local-development)
- [🔧 Environment Variables](#-environment-variables)
- [🗄️ Database](#️-database)
- [☁️ File Storage](#️-file-storage)
- [🚀 Deployment](#-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👤 Author](#-author)

---

## 🎯 Motive & Vision

> **"Every developer has a story worth telling — they just need the right platform to tell it."**

Most developers spend days or weeks building their own portfolio websites from scratch, only to abandon them when they get busy, or end up with outdated information scattered across PDFs, LinkedIn, and GitHub. **Multi-User Portfolio** solves this completely.

This platform is designed to be the **single source of truth** for a developer's professional identity. Instead of rebuilding a site every time you switch jobs, learn a new skill, or complete a new project — you simply log in, update your dashboard, and your portfolio is instantly live at a clean, shareable URL.

### The Problem We Solve

| Old Way | Multi-User Portfolio Way |
|---|---|
| Build a portfolio site from scratch every time | Register once, update anytime |
| Manually update PDF resumes | Live portfolio always reflects latest info |
| Pay for hosting + domain just for a portfolio | Free, instant deployment |
| Different link for every version | One permanent URL: `/your-username/` |
| No structure for projects/experience | Guided dashboard for every section |

### Who Is This For?

- 🎓 **Students** building their first professional presence
- 💼 **Developers** who want a clean, maintained portfolio without the maintenance overhead
- 🔍 **Job seekers** who need a shareable, professional link ready at any time
- 👨‍💻 **Freelancers** who want to showcase their work to clients

---

## ✨ Features

### 👤 Multi-User System
- Secure registration with a unique public slug (`/your-username/`)
- Each user gets a fully isolated portfolio — data never leaks between accounts
- Publish/unpublish control — go live only when you're ready
- Reserved word protection (no one can claim `/admin`, `/login`, etc.)

### 📊 Complete Portfolio Management Dashboard
- **Personal Info** — name, tagline, bio, location, years of experience, open-to-work badge
- **Projects** — title, description, type, status, live URL, repo URL, thumbnail, cover image, technologies, tags, featured flag
- **Experience** — company, role, employment type, remote flag, dates, technologies, company logo
- **Education** — institution, degree, field of study, grade, dates, institution logo
- **Skills** — categorized skills with proficiency levels and Devicon icon classes
- **Social Links** — GitHub, LinkedIn, Twitter/X, Instagram, personal website, with live icons
- **Contact Messages** — public contact form per portfolio, all messages viewable in dashboard

### 🖼️ File Uploads
- Profile photo (image)
- Resume (PDF download)
- Project thumbnails and cover images
- Company and institution logos
- Skill icons
- All stored persistently on **Cloudinary** — never lost on redeployment

### 🌐 Public Portfolio Page
- Fully rendered public page at `/{slug}/`
- Shows published state: coming-soon page for unpublished portfolios
- Clean 404 for usernames that don't exist

### 🔒 Security
- Django's built-in CSRF protection on every form
- `login_required` on all dashboard views
- User-scoped querysets — users can only see/edit their own data
- Production-safe settings: `DEBUG=False`, env-var-driven secrets, `SECURE_PROXY_SSL_HEADER`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django 5.2 (Python 3.12) |
| **Database** | PostgreSQL (production) / SQLite (local dev) |
| **File Storage** | Cloudinary |
| **Static Files** | WhiteNoise |
| **Web Server** | Gunicorn |
| **Hosting** | Render |
| **Auth** | Django's built-in `django.contrib.auth` |
| **Image Processing** | Pillow |
| **Env Management** | python-dotenv |

---

## 📁 Project Structure

```
Multi-User-Portfolio/
│
├── portfolio/                  # Main Django app + project package
│   ├── migrations/             # Database migrations
│   ├── templates/
│   │   ├── layout.html         # Base template (nav, footer, CSS variables)
│   │   ├── dashboard/          # All dashboard page templates
│   │   │   ├── base.html       # Dashboard layout with sidebar
│   │   │   ├── overview.html
│   │   │   ├── personal.html
│   │   │   ├── projects.html
│   │   │   ├── project_form.html
│   │   │   ├── experience.html
│   │   │   ├── education.html
│   │   │   ├── skills.html
│   │   │   ├── social.html
│   │   │   └── messages.html
│   │   ├── website/            # Public-facing templates
│   │   │   ├── landing.html
│   │   │   ├── portfolio.html
│   │   │   ├── coming_soon.html
│   │   │   └── not_found.html
│   │   └── auth/               # Login & register templates
│   │       ├── login.html
│   │       └── register.html
│   ├── models.py               # All data models
│   ├── views.py                # All views (auth, dashboard, public)
│   ├── forms.py                # ModelForms for all sections
│   ├── urls.py                 # URL routing
│   ├── signals.py              # Auto-creates UserProfile + PersonalInfo on register
│   ├── apps.py                 # AppConfig (wires signals.py)
│   ├── admin.py                # Django admin registrations
│   ├── settings.py             # Project settings (env-var driven)
│   ├── wsgi.py
│   └── asgi.py
│
├── manage.py
├── requirements.txt
├── Procfile                    # Gunicorn start command for Render
├── runtime.txt                 # Python version pin (3.12.7)
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start (Local Development)

### Prerequisites

- Python 3.12+
- Git
- (Optional) A Cloudinary account for testing file uploads

### 1. Clone the repository

```bash
git clone https://github.com/prashantraj09/Multi-User-Portfolio.git
cd Multi-User-Portfolio/portfolio
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a file named `.env` in the same folder as `manage.py`:

```env
SECRET_KEY=your-local-dev-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=
DATABASE_URL=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

> **Note:** `DATABASE_URL` blank → auto-uses SQLite. `CLOUDINARY_*` blank → uploads go to local `/media/` folder. Both are fine for local development.

### 5. Run migrations and start the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — register a user, fill in your details, and visit `/{your-slug}/` to see your public portfolio.

---

## 🔧 Environment Variables

| Variable | Required in Production | Description |
|---|---|---|
| `SECRET_KEY` | ✅ Yes | Django secret key — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | ✅ Yes | Set to `False` in production |
| `ALLOWED_HOSTS` | ✅ Yes | Comma-separated list of allowed hostnames, e.g. `your-app.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | ✅ Yes | Full URL including scheme, e.g. `https://your-app.onrender.com` |
| `DATABASE_URL` | ✅ Yes | Postgres connection string from your host. Blank = falls back to SQLite |
| `CLOUDINARY_CLOUD_NAME` | ✅ Yes (for uploads) | From your Cloudinary dashboard |
| `CLOUDINARY_API_KEY` | ✅ Yes (for uploads) | From your Cloudinary dashboard |
| `CLOUDINARY_API_SECRET` | ✅ Yes (for uploads) | From your Cloudinary dashboard |

---

## 🗄️ Database

The project uses **PostgreSQL** in production and falls back to **SQLite** for local development automatically — no code changes needed between environments.

In production on Render, use the **Internal Database URL** (not External) for better performance and no egress charges.

```python
# settings.py automatically handles this:
_DATABASE_URL = os.environ.get('DATABASE_URL', '').strip()
if _DATABASE_URL:
    DATABASES = {'default': dj_database_url.parse(_DATABASE_URL)}
else:
    DATABASES = {'default': {'ENGINE': 'sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
```

---

## ☁️ File Storage

All uploaded files (profile photos, project thumbnails, resumes, logos) are stored on **Cloudinary** when credentials are present, ensuring they survive redeployments.

When Cloudinary credentials are absent (local dev with no `.env`), files are stored on the local filesystem in the `media/` directory.

```
portfolio/profile/       → Profile photos
portfolio/resume/        → Resume PDFs
portfolio/projects/      → Project thumbnails and covers
portfolio/experience/    → Company logos
portfolio/education/     → Institution logos
portfolio/skills/        → Skill icons
```

---

## 🚀 Deployment

This project is configured to deploy on **[Render](https://render.com)** out of the box.

### Steps

1. **Fork / push this repo** to your GitHub account.
2. Create a **PostgreSQL** instance on Render (free tier) → copy the Internal Database URL.
3. Create a **Web Service** on Render → connect your GitHub repo.
4. Set the following in the Web Service:

   | Setting | Value |
   |---|---|
   | **Root Directory** | `portfolio` |
   | **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
   | **Start Command** | `gunicorn portfolio.wsgi --log-file -` |

5. Add all environment variables from the [table above](#-environment-variables) in the **Environment** tab.
6. Add `PYTHON_VERSION=3.12.7` to pin the Python version.
7. Deploy — your app will be live at `https://your-service-name.onrender.com`.

> **Free tier note:** Render free services spin down after 15 minutes of inactivity. The first visitor after a sleep period may experience a ~30s cold start. This does **not** affect data — the database is a separate persistent service.

---


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork this repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "feat: add your feature description"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a **Pull Request** — describe what you changed and why.

### Ideas for Contribution

- [ ] Dark/light mode toggle
- [ ] PDF export of the portfolio page
- [ ] Analytics (page view counts per portfolio)
- [ ] Custom domains per user
- [ ] Portfolio themes / templates
- [ ] API endpoints (DRF is already installed)

---

## 📄 License

This project is licensed under the **MIT License** — you're free to use, modify, and distribute it. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

<div align="center">

**Prashant Raj**

[![GitHub](https://img.shields.io/badge/GitHub-prashantraj09-181717?style=for-the-badge&logo=github)](https://github.com/prashantraj09)

*Built with ❤️ and a lot of debugging.*

---

⭐ **If this project helped you, please give it a star on GitHub!** ⭐

</div>
