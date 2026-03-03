# Local VFC — PythonAnywhere Deployment Guide

This guide walks you through deploying Local VFC to PythonAnywhere free hosting.

## Prerequisites

- PythonAnywhere account (free tier: https://pythonanywhere.com)
- GitHub repo with code pushed
- Google OAuth credentials (from Google Cloud Console)
- Retell AI API keys (optional, but required for voice search feature)

---

## Step 1 — Clone & Setup in PythonAnywhere Bash Console

Open PythonAnywhere bash console and run:

```bash
cd ~
git clone https://github.com/yourusername/local-vfc.git
cd "local-vfc/local vfc"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Step 2 — Create Database & Migrate

Still in bash, with virtualenv activated:

```bash
python manage.py migrate
python manage.py seed_categories
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Create admin account
```

---

## Step 3 — Configure Web App in PythonAnywhere

### Source Code & Virtualenv
1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose "Manual configuration" → Python 3.11
4. In the configuration:
   - **Source code:** `/home/yourusername/local-vfc/local vfc`
   - **Virtualenv:** `/home/yourusername/local-vfc/local vfc/.venv`

### WSGI File Configuration
1. Edit **WSGI configuration file** (appears in Web tab)
2. **Delete all content** and paste this instead:

```python
import os
import sys

path = '/home/yourusername/local-vfc/local vfc'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. **Save** the WSGI file
4. Click **Reload** in Web tab

---

## Step 4 — Set Environment Variables

In PythonAnywhere **Web** tab:

Add these under "Web app security settings" or in a bash console:

```bash
export SECRET_KEY='your-random-50-character-string-here'
export DEBUG='False'
export GOOGLE_CLIENT_ID='your-google-client-id'
export GOOGLE_CLIENT_SECRET='your-google-client-secret'
export RETELL_API_KEY='your-retell-key'
export RETELL_AGENT_ID='your-retell-agent-id'
```

Or edit `.env` file in your project directory directly via bash:

```bash
nano local\ vfc/.env
```

Add your actual credentials there.

---

## Step 5 — Configure Static & Media Files

In **Web** tab, under "Static files (← keep this before your web app):

1. **URL:** `/static/` → **Directory:** `/home/yourusername/local-vfc/local vfc/staticfiles`
2. **URL:** `/media/` → **Directory:** `/home/yourusername/local-vfc/local vfc/media`

Click **Reload** after adding.

---

## Step 6 — Test Your Deployment

1. Click **Reload** in Web tab
2. Visit your URL: `https://yourusername.pythonanywhere.com`
3. Check **Error log** in Web tab if issues appear

### Common Issues:
- **500 Error:** Check error log and `python manage.py check --deploy`
- **Static files not loading:** Run `python manage.py collectstatic --noinput` again
- **Database locked:** Remove old `db.sqlite3` and migrate fresh

---

## Step 7 — Update After Code Changes

When you push updates to GitHub:

```bash
cd ~/local-vfc/local\ vfc
source .venv/bin/activate
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload** in PythonAnywhere **Web** tab.

---

## Admin Panel Access

Visit: `https://yourusername.pythonanywhere.com/admin`

Login with the superuser account you created in Step 2.

---

## Troubleshooting

### View Error Logs
- PythonAnywhere **Web** tab → **Error log** (bottom of page)
- Or in bash: `tail -f /var/log/yourusername.pythonanywhere.com.log`

### Check Django Configuration
```bash
python manage.py check --deploy
```

### Debug in Bash
```bash
source .venv/bin/activate
cd local\ vfc
python manage.py shell
# Test imports, queries, etc.
```

### Restart the Web App
In **Web** tab, click **Reload** (sometimes fixes connection issues)

---

## Security Checklist

- ✅ Change `SECRET_KEY` to a random 50-character string
- ✅ Set `DEBUG=False` in production
- ✅ Use environment variables for all sensitive data
- ✅ Keep `.env` in `.gitignore` (don't commit secrets!)
- ✅ Use `https://` (PythonAnywhere provides SSL by default)
- ✅ Create strong superuser password
- ✅ Review `CSRF_TRUSTED_ORIGINS` in `settings.py`

---

## Next Steps

1. Configure Google OAuth to accept your PythonAnywhere domain
2. Test all major features (vendor search, reviews, voice search)
3. Monitor error logs for first week
4. Set up regular backups of `db.sqlite3`

---

## Support

- **PythonAnywhere Help:** https://pythonanywhere.com/help/
- **Django Deployment:** https://docs.djangoproject.com/en/5.2/howto/deployment/
- **WhiteNoise Docs:** https://whitenoise.readthedocs.io/

---

**Deployed with ❤️ on PythonAnywhere**
