# 🚀 QUICK START — Deploy to PythonAnywhere

## ⚡ 5-Minute Summary

Your Local VFC app is **ready for production**. Here's what to do RIGHT NOW:

---

## 1️⃣ Generate & Add SECRET_KEY (2 minutes)

Run this in terminal:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Copy the output, then edit `.env`:
```
SECRET_KEY=<paste-the-long-random-string-here>
DEBUG=False
```

---

## 2️⃣ Test Locally (1 minute)

```bash
python manage.py check --deploy
python manage.py runserver
```

Visit http://localhost:8000 and verify it loads. ✅

---

## 3️⃣ Commit to GitHub (1 minute)

```bash
git add .
git commit -m "Configure for PythonAnywhere deployment"
git push origin main
```

---

## 4️⃣ Deploy to PythonAnywhere (20-30 minutes)

### **Open DEPLOYMENT.md and follow Steps 1-7**

It's detailed but easy. You'll:
- Create PythonAnywhere account
- Clone your repo
- Configure Python environment
- Run migrations
- Set up web app
- Get your site live!

---

## 📚 What Files to Read

1. **DEPLOYMENT.md** — Complete step-by-step guide (START HERE)
2. **DEPLOYMENT_CHECKLIST.md** — Quick reference checklist
3. **DEPLOYMENT_SUMMARY.md** — Overview of all changes
4. **wsgi_pythonanywhere.py** — WSGI config template (copy to PythonAnywhere)

---

## ✅ Verification Checklist

Before you start:
- [ ] Edit `.env` with random SECRET_KEY
- [ ] Verify `DEBUG=False` in `.env`
- [ ] Run `python manage.py check --deploy`
- [ ] Test locally with `python manage.py runserver`
- [ ] Commit and push to GitHub
- [ ] Have your Google OAuth credentials ready
- [ ] Have your Retell AI keys ready (if using voice search)

---

## 🎯 WhatsIncluded?

✅ **Django optimization**
- WhiteNoise for static file serving
- Security headers for HTTPS
- Environment variable configuration

✅ **Files created**
- Procfile (for reference)
- wsgi_pythonanywhere.py (copy to PythonAnywhere)
- DEPLOYMENT.md (complete guide)
- .env.example (safe template)

✅ **Configuration updated**
- settings.py (production-ready)
- .env (with DEBUG=False)
- requirements.txt (includes whitenoise)
- .gitignore (secure)

✅ **Static files**
- 167 files collected and optimized
- Ready for instant serving

---

## 🚨 IMPORTANT

**3 Things to DO RIGHT NOW:**

1. ⚠️ Generate & update SECRET_KEY in `.env`
2. ⚠️ Test locally (`python manage.py runserver`)
3. ⚠️ Commit & push to GitHub

**3 Things to NOT do:**

1. ❌ Don't commit the `.env` file (it's in .gitignore)
2. ❌ Don't skip the SECRET_KEY generation
3. ❌ Don't deploy without testing locally first

---

## 💡 Pro Tips

- Keep `.env` for real credentials locally
- Use `.env.example` as a template for teammates
- Monitor PythonAnywhere error logs during first deployment
- Test main features after deployment (search, auth, reviews)
- Keep your GitHub repo updated as you make changes

---

## 🔗 Resources

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** — Full step-by-step guide
- **[PythonAnywhere Free Tier](https://www.pythonanywhere.com)** — Where to deploy
- **[wsgi_pythonanywhere.py](./wsgi_pythonanywhere.py)** — WSGI template
- **requirements.txt** — All dependencies (132 packages)

---

## ❓ Help!

If something breaks:

1. Check **PythonAnywhere error log** (in Web tab)
2. Run `python manage.py check --deploy` locally
3. Read **DEPLOYMENT_CHECKLIST.md** troubleshooting section
4. Re-read **DEPLOYMENT.md** Step 2 (database setup)

---

**Let's go! Your app is ready. 🚀**

Follow DEPLOYMENT.md and you'll be live in 30 minutes!
