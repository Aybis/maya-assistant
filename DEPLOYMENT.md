# Maya Assistant - Render Deployment Guide

This guide walks you through deploying the Maya Assistant application to Render, a modern cloud platform that supports both backend and frontend deployments.

## 📋 Prerequisites

- Render account (sign up at [render.com](https://render.com))
- GitHub account with this repository
- Supabase project (for database and authentication)
- API keys for AI providers (OpenAI, Anthropic, and/or Google AI)

## 🏗️ Architecture Overview

Maya Assistant consists of two services on Render:
1. **Backend (Web Service)**: FastAPI application
2. **Frontend (Static Site)**: Next.js application

---

## 🚀 Step 1: Deploy Backend (FastAPI)

### 1.1 Create New Web Service

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

### 1.2 Backend Configuration

| Setting | Value |
|---------|-------|
| **Name** | `maya-assistant-backend` |
| **Region** | Choose closest to your users |
| **Branch** | `main` (or your production branch) |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | Free or Starter (upgrade as needed) |

### 1.3 Backend Environment Variables

Add these environment variables in Render dashboard:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_JWT_SECRET=your-supabase-jwt-secret

# AI Provider API Keys (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# CORS Configuration
CORS_ORIGINS=https://your-frontend-url.onrender.com,http://localhost:3000

# Application Settings
APP_NAME=Maya Assistant
APP_VERSION=1.0.0
DEBUG=false
HOST=0.0.0.0
PORT=10000
```

**Important Notes:**
- The `PORT` environment variable is automatically set by Render
- Update `CORS_ORIGINS` after deploying frontend (see Step 2)
- Keep your JWT secret secure and different from your Supabase anon key

### 1.4 Deploy Backend

1. Click **"Create Web Service"**
2. Wait for the build and deployment to complete
3. Note your backend URL: `https://maya-assistant-backend.onrender.com`

### 1.5 Verify Backend Deployment

Test your backend:
```bash
curl https://maya-assistant-backend.onrender.com/
```

Expected response:
```json
{
  "name": "Maya Assistant",
  "version": "1.0.0",
  "status": "running"
}
```

---

## 🎨 Step 2: Deploy Frontend (Next.js)

### 2.1 Create New Static Site

1. Go to Render Dashboard
2. Click **"New +"** → **"Static Site"**
3. Connect the same GitHub repository
4. Configure the service:

### 2.2 Frontend Configuration

| Setting | Value |
|---------|-------|
| **Name** | `maya-assistant-frontend` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `frontend` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `out` |

### 2.3 Update Next.js for Static Export

Before deploying, ensure your `frontend/next.config.js` has:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Enable static export
  images: {
    unoptimized: true,  // Required for static export
  },
}

module.exports = nextConfig
```

### 2.4 Frontend Environment Variables

Add these environment variables:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
NEXT_PUBLIC_API_URL=https://maya-assistant-backend.onrender.com
```

**Important:** Replace the backend URL with your actual Render backend URL from Step 1.4.

### 2.5 Deploy Frontend

1. Click **"Create Static Site"**
2. Wait for build and deployment
3. Note your frontend URL: `https://maya-assistant-frontend.onrender.com`

### 2.6 Update Backend CORS

Go back to your backend service and update the `CORS_ORIGINS` environment variable:

```bash
CORS_ORIGINS=https://maya-assistant-frontend.onrender.com
```

This allows your frontend to communicate with the backend.

---

## 🗄️ Step 3: Configure Supabase

### 3.1 Update Supabase Redirect URLs

1. Go to your [Supabase Dashboard](https://app.supabase.com)
2. Navigate to **Authentication** → **URL Configuration**
3. Add your frontend URL to **Site URL**:
   ```
   https://maya-assistant-frontend.onrender.com
   ```
4. Add to **Redirect URLs**:
   ```
   https://maya-assistant-frontend.onrender.com/auth/callback
   ```

### 3.2 Configure OAuth Provider

Enable Google OAuth:
1. Go to **Authentication** → **Providers**
2. Enable **Google**
3. Add authorized redirect URI:
   ```
   https://your-project.supabase.co/auth/v1/callback
   ```

---

## 🔒 Step 4: Secure Your Deployment

### 4.1 Environment Variable Security

✅ **Do's:**
- Store all secrets as environment variables in Render
- Use different keys for production vs development
- Rotate API keys periodically
- Use Render's secret file feature for sensitive data

❌ **Don'ts:**
- Never commit `.env` files to git
- Don't share API keys in public repositories
- Don't use development keys in production

### 4.2 CORS Configuration

Ensure backend only accepts requests from your frontend:

```bash
CORS_ORIGINS=https://maya-assistant-frontend.onrender.com
```

For multiple domains:
```bash
CORS_ORIGINS=https://maya-assistant-frontend.onrender.com,https://custom-domain.com
```

---

## 📊 Step 5: Monitoring and Logs

### 5.1 View Logs

**Backend Logs:**
1. Go to Render Dashboard → `maya-assistant-backend`
2. Click **"Logs"** tab
3. Monitor real-time logs for errors or issues

**Frontend Logs:**
1. Go to Render Dashboard → `maya-assistant-frontend`
2. Click **"Logs"** tab
3. Check build logs for any issues

### 5.2 Health Checks

Render automatically performs health checks on your services.

**Backend Health Check:**
- Endpoint: `GET /` or `GET /api/health`
- Should return 200 status code

### 5.3 Monitoring

Set up monitoring:
- Enable email notifications for deployment failures
- Monitor error rates in logs
- Track API usage with AI providers

---

## 🔄 Step 6: Continuous Deployment

### 6.1 Auto-Deploy Setup

Render automatically deploys when you push to your configured branch:

1. **Backend**: Pushes to `main` trigger backend rebuild
2. **Frontend**: Pushes to `main` trigger frontend rebuild

### 6.2 Deploy Hooks

Create manual deploy hooks:
1. Go to service settings → **Deploy Hook**
2. Copy the webhook URL
3. Use to trigger deployments via API or CI/CD

### 6.3 Branch Deployments

For preview environments:
1. Create a new branch (e.g., `staging`)
2. Set up separate Render services for staging
3. Use different environment variables

---

## 🌐 Step 7: Custom Domain (Optional)

### 7.1 Add Custom Domain to Frontend

1. Go to `maya-assistant-frontend` settings
2. Click **"Custom Domains"**
3. Add your domain: `maya.yourdomain.com`
4. Configure DNS:
   - **CNAME Record**: Point to Render URL
   - Wait for SSL certificate to provision

### 7.2 Add Custom Domain to Backend

1. Go to `maya-assistant-backend` settings
2. Add backend domain: `api.yourdomain.com`
3. Update environment variables:
   ```bash
   # Frontend
   NEXT_PUBLIC_API_URL=https://api.yourdomain.com

   # Backend
   CORS_ORIGINS=https://maya.yourdomain.com
   ```

---

## 🧪 Step 8: Testing Deployment

### 8.1 Test Backend

```bash
# Health check
curl https://maya-assistant-backend.onrender.com/

# List available models
curl https://maya-assistant-backend.onrender.com/api/models
```

### 8.2 Test Frontend

1. Open `https://maya-assistant-frontend.onrender.com`
2. Sign in with Google
3. Create a new conversation
4. Send a message to verify AI integration
5. Check browser console for errors

### 8.3 Test End-to-End

Complete user flow:
1. ✅ User can sign in
2. ✅ User can create conversation
3. ✅ User can select AI model
4. ✅ User can send message
5. ✅ AI response streams correctly
6. ✅ Conversation persists on reload

---

## ⚡ Performance Optimization

### Backend Optimization

```python
# Add to app/main.py for better production performance
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Frontend Optimization

Ensure optimal Next.js build:
```json
// package.json
{
  "scripts": {
    "build": "next build && next export"
  }
}
```

---

## 🐛 Troubleshooting

### Common Issues

#### Backend not starting
```
Error: Port already in use
```
**Solution:** Ensure start command uses `$PORT`:
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### CORS errors
```
Access to fetch blocked by CORS policy
```
**Solution:** Add frontend URL to `CORS_ORIGINS`:
```bash
CORS_ORIGINS=https://your-frontend.onrender.com
```

#### Environment variables not loading
**Solution:** Check:
- Variables are set in Render dashboard
- Service was redeployed after adding variables
- No typos in variable names

#### 502 Bad Gateway
**Solution:**
- Check backend logs for crashes
- Verify all required dependencies in `requirements.txt`
- Ensure database connection is working

#### Build failures
**Solution:**
- Check build logs in Render
- Verify `requirements.txt` (backend) or `package.json` (frontend)
- Ensure Python version compatibility

---

## 💰 Cost Estimation

### Free Tier
- **Backend**: Free tier available (spins down after inactivity)
- **Frontend**: Free for static sites
- **Total**: $0/month (with limitations)

### Starter Plan
- **Backend**: $7/month (always on, faster)
- **Frontend**: Free
- **Total**: $7/month

### Production Plan
- **Backend**: $25/month (2GB RAM, auto-scaling)
- **Frontend**: Free
- **Database**: Use Supabase free tier or paid
- **Total**: $25+/month

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Static Export](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [Supabase Auth](https://supabase.com/docs/guides/auth)

---

## 🎯 Deployment Checklist

Before going live, verify:

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables configured correctly
- [ ] Supabase redirect URLs updated
- [ ] Google OAuth configured
- [ ] CORS settings properly configured
- [ ] All AI provider API keys working
- [ ] SSL certificates active (HTTPS)
- [ ] Health checks passing
- [ ] End-to-end testing completed
- [ ] Error monitoring setup
- [ ] Backup strategy in place

---

## 🆘 Support

For issues:
1. Check Render status page: [status.render.com](https://status.render.com)
2. Review Render logs for errors
3. Check Supabase project status
4. Verify AI provider API status

---

**Congratulations!** 🎉 Your Maya Assistant is now deployed on Render!

Visit your live application at: `https://maya-assistant-frontend.onrender.com`
