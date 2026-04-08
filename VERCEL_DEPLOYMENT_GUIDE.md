# 🚀 Deploying Krishi Drishti to Vercel

## ⚠️ Important: Static Vercel Strategy

This repository now includes a **fully static Vercel-ready frontend**:

1. `index.html` → Prediction interface
2. `analytics.html` → Advanced analytics dashboard
3. `analytics-static.js` → Browser-based analytics logic

The homepage button now opens the static analytics dashboard, so the full user experience works on Vercel without Streamlit.

---

## 📋 Prerequisites

1. **GitHub Account** - https://github.com
2. **Vercel Account** - https://vercel.com (sign up with GitHub)
3. **Streamlit Cloud Account** - https://streamlit.io/cloud (for dashboard)
4. **Git Installed** - https://git-scm.com/

---

## 🔧 Part 1: Deploy the Static Site to Vercel

### Step 1: Prepare Repository

```bash
cd C:\Users\ay840\Downloads\KRISHI-DRISTI-2.0

# Initialize Git
git init
git add .
git commit -m "Initial commit - Vercel deployment"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Name: `krishi-drishti`
3. Create repository (don't initialize)
4. Push your code:

```bash
git remote add origin https://github.com/YOUR-USERNAME/krishi-drishti.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy the Static Site to Vercel

1. Go to https://vercel.com/dashboard
2. Click **"New Project"**
3. **Import** your `krishi-drishti` repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as root)
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)

5. No environment variables are required for the static frontend.

6. Click **"Deploy"**
7. Wait 2-3 minutes
8. Your site will be live at: `https://krishi-drishti-YOUR-USERNAME.vercel.app`

### Step 4: Test Your Site

Visit: `https://krishi-drishti-YOUR-USERNAME.vercel.app`

You should see the prediction interface, and the Analytics Dashboard button should open `analytics.html`.

---

## 🎨 Part 2: Optional Streamlit Dashboard

### Step 1: Sign Up for Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with GitHub
3. Authorize Streamlit

### Step 2: Deploy Dashboard

1. Click **"New app"**
2. Select your repository: `krishi-drishti`
3. Configure:
   - **Branch**: `main`
   - **Main file path**: `frontend/dashboard.py`
   - **App URL**: Choose your custom URL

4. **Advanced settings** → Add environment variable:
   ```
   API_BASE_URL = https://krishi-drishti-YOUR-USERNAME.vercel.app/api/v1
   ```
   *(Replace with your actual Vercel URL from Part 1)*

5. Click **"Deploy!"**
6. Wait 2-3 minutes
7. Your dashboard will be live at: `https://YOUR-APP.streamlit.app`

---

## 🔄 Alternative: All-Vercel Deployment (HTML Frontend)

If you want everything on Vercel, use the static files already included in this repository:

- `index.html` for predictions
- `analytics.html` for advanced analytics
- `analytics-static.js` for chart and dashboard logic

This setup is already Vercel-friendly and does not require Streamlit for the deployed site.

---

## 📊 After Deployment

### Your Live URLs:

**Recommended Setup:**
- 🌐 **Static Site**: `https://krishi-drishti-YOUR-USERNAME.vercel.app`
- 📊 **Analytics Dashboard**: `https://krishi-drishti-YOUR-USERNAME.vercel.app/analytics.html`

---

## 🎯 Vercel-Specific Notes

### Limitations:
1. **Serverless Functions**: 
   - Max execution time: 10 seconds (Hobby), 60s (Pro)
   - Max payload: 4.5 MB
   - Cold starts: First request may be slower

2. **Model Files**:
   - `.joblib` files must be < 50MB each
   - If larger, use external storage (AWS S3, etc.)

3. **No Websockets**:
   - Streamlit needs persistent connections
   - That's why we use Streamlit Cloud for dashboard

### Advantages:
- ⚡ Extremely fast (Edge Network)
- 🌍 Global CDN
- 🔄 Auto-deploy on git push
- 🆓 Generous free tier
- 💪 Automatic HTTPS

### Included Static Pages:
- `index.html` - Prediction interface
- `analytics.html` - Advanced analytics dashboard
- `all_crop_data.csv` - Data source used by the browser analytics logic

---

## 🔧 Update & Redeploy

After making changes:

```bash
git add .
git commit -m "Your update message"
git push
```

Both Vercel and Streamlit Cloud will auto-deploy!

---

## 📝 Required Files (Already Created!)

✅ `vercel.json` - Vercel configuration
✅ `index.py` - Entry point for Vercel
✅ `api/index.py` - Serverless function wrapper
✅ `backend/requirements.txt` - Python dependencies
✅ Updated `backend/app.py` - PORT environment variable support
✅ Updated `frontend/dashboard.py` - API_BASE_URL environment variable

---

## 🐛 Troubleshooting

### Issue: "Module not found" on Vercel
**Solution**: Make sure all required packages are in requirements.txt
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### Issue: Dashboard can't connect to API
**Solution**: 
1. Go to Streamlit Cloud dashboard
2. Open your app settings
3. Update `API_BASE_URL` environment variable
4. Must match your Vercel URL exactly (include `/api/v1`)

### Issue: "Function timeout"
**Solution**: 
- Reduce model size
- Optimize predictions
- Cache results
- Or upgrade to Vercel Pro ($20/month for 60s timeout)

### Issue: Model files too large (>50MB)
**Solution**: 
- Compress models using joblib with compression
- Or store models in AWS S3/Cloudflare R2 and load at runtime
- Or split into smaller regional deployments

### Issue: Build fails on Vercel
**Solution**: 
1. Check Vercel logs in dashboard
2. Verify Python version (3.11)
3. Check all imports are in requirements.txt
4. Make sure vercel.json is in root directory

---

## 💡 Recommended Setup

**Best Performance & Cost:**

| Component | Platform | Why | Cost |
|-----------|----------|-----|------|
| Backend API | Vercel | Fast global edge, serverless | Free |
| Dashboard | Streamlit Cloud | Native Streamlit support | Free |
| Models | In repo | < 50MB works fine | Free |

---

## 🎁 Bonus: Custom Domain

### For Vercel:
1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records (Vercel provides instructions)
5. HTTPS automatic!

### For Streamlit Cloud:
- Custom domains available on Teams/Enterprise plans
- Or use subdomain: `your-app.streamlit.app`

---

## 📞 Quick Commands Reference

```bash
# First time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/krishi-drishti.git
git push -u origin main

# Updates
git add .
git commit -m "Update message"
git push

# Check git status
git status

# View commit history
git log --oneline

# Install Vercel CLI (optional)
npm i -g vercel
vercel login
vercel --prod
```

---

## 🚀 Quick Start Summary

1. **Push to GitHub** (5 minutes)
2. **Deploy Backend to Vercel** (3 minutes)  
3. **Deploy Dashboard to Streamlit Cloud** (3 minutes)

**Total time**: ~10 minutes!
**Total cost**: FREE! 🎉

---

## 🔗 Helpful Links

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Streamlit Cloud**: https://share.streamlit.io
- **Vercel Docs**: https://vercel.com/docs/frameworks/custom-deployments
- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **FastAPI on Vercel**: https://vercel.com/guides/using-fastapi-with-vercel

---

## 🎯 Step-by-Step Checklist

### Phase 1: Preparation
- [ ] Install Git
- [ ] Create GitHub account
- [ ] Create Vercel account
- [ ] Create Streamlit Cloud account

### Phase 2: Repository Setup
- [ ] Initialize Git repository
- [ ] Create GitHub repository
- [ ] Push code to GitHub

### Phase 3: Backend Deployment
- [ ] Import project to Vercel
- [ ] Add environment variables
- [ ] Deploy backend
- [ ] Test API endpoint
- [ ] Copy API URL

### Phase 4: Dashboard Deployment
- [ ] Create new app on Streamlit Cloud
- [ ] Select repository
- [ ] Configure main file path
- [ ] Add API_BASE_URL environment variable
- [ ] Deploy dashboard

### Phase 5: Testing
- [ ] Test backend API
- [ ] Test dashboard
- [ ] Test predictions
- [ ] Test all crops/states
- [ ] Verify weather API integration

---

## 🆘 Need Help?

**Problem**: Not sure which platform to use?
**Recommendation**: 
- Use Vercel for backend (it's faster)
- Use Streamlit Cloud for dashboard (it's easier)
- This combination is FREE and works great!

**Problem**: Want everything on one platform?
**Options**:
1. Use Render for both (see RENDER_DEPLOYMENT_GUIDE.md)
2. Request HTML frontend for all-Vercel deployment
3. Use Heroku (requires credit card but still free tier available)

**Problem**: Models are too large
**Solution**:
- Current models should be fine (< 10MB each)
- If needed, I can help set up S3 storage
- Or compress models further

---

## 📈 After Deployment Benefits

### Global Availability
- Your API accessible worldwide
- Fast response times via CDN
- 99.9% uptime

### Auto-Scaling
- Handles traffic spikes automatically
- No server management needed
- Scales to zero when not in use (free!)

### Version Control
- Every deploy creates a unique URL
- Easy rollback to previous versions
- Preview deployments for testing

### Monitoring
- Built-in analytics
- Error tracking
- Performance metrics

---

## 🎉 Success Checklist

After deployment, you should have:
- ✅ Live backend API with documentation
- ✅ Live interactive dashboard
- ✅ Automatic deployments on git push
- ✅ HTTPS enabled by default
- ✅ Global CDN distribution
- ✅ All for FREE!

---

**Ready to deploy?** Start with Part 1! 🚀

**Questions?** Check the troubleshooting section or refer to:
- VERCEL_CHECKLIST.md (step-by-step checklist)
- DEPLOY.md (quick commands)
- RENDER_DEPLOYMENT_GUIDE.md (alternative platform)