# 🤖 MCPs + Agents Demo - Cloudflare Deployment

This is a containerized version of the MCPs + Agents Demo, optimized for Cloudflare Container deployment.

## 🚨 Current Status

**Cloudflare Containers requires a paid Workers plan ($5/month minimum)**

The deployment failed with "Unauthorized" because Cloudflare Containers is only available on paid plans.

## 🚀 Deployment Options

### Option 1: Cloudflare Containers (Paid - $5/month)

**Requirements:**
- Cloudflare Workers Standard plan ($5/month)
- Docker installed locally

**Steps:**
1. Upgrade your Cloudflare account to Workers Standard
2. Run `wrangler deploy`

**Benefits:**
- Global edge deployment (320+ cities)
- Pay-per-use billing
- Auto-scaling from 0
- Integrated security

### Option 2: Alternative Free Deployments

Since Cloudflare Containers requires payment, here are free alternatives:

#### A. Railway (Free Tier Available)
```bash
# Use the Railway configuration from the parent directory
cd ..
railway login
railway link
railway up
```

#### B. Render (Free Tier)
```bash
# Deploy to Render using Docker
# 1. Connect your GitHub repo to Render
# 2. Use this Dockerfile for deployment
```

#### C. Fly.io (Free Tier)
```bash
# Install flyctl and deploy
fly auth login
fly launch
fly deploy
```

## 🔧 Current Configuration

This container is configured for:
- **Production mode**: Users must provide their own API keys
- **Security**: No default keys in production
- **Streamlit optimization**: Proper health checks and startup
- **Global deployment**: Ready for Cloudflare's edge network

## 📁 Files Overview

- `Dockerfile` - Optimized for Cloudflare Containers
- `wrangler.jsonc` - Cloudflare configuration
- `src/index.ts` - Worker code for routing
- `apps/` - Streamlit application code
- `CLOUDFLARE_DEPLOYMENT.md` - Detailed deployment guide

## 🔑 Security Features

- ✅ Production mode enforced in container
- ✅ No default API keys in production
- ✅ Client-side key storage only
- ✅ Rate limiting built-in
- ✅ Secure container configuration

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier | Global Edge |
|----------|-----------|-----------|-------------|
| **Cloudflare Containers** | ❌ | $5/month + usage | ✅ 320+ cities |
| **Railway** | 500 hours/month | $5/month | ❌ Single region |
| **Render** | 750 hours/month | $7/month | ❌ Single region |
| **Fly.io** | 160GB-hours | $1.94/month | ✅ Global |

## 🎯 Recommendation

**For Free Deployment**: Use Railway or Render with the parent directory configuration
**For Global Performance**: Upgrade to Cloudflare Workers Standard ($5/month)

## 📚 Next Steps

1. **Free Option**: Go back to parent directory and deploy to Railway
2. **Paid Option**: Upgrade Cloudflare plan and run `wrangler deploy`
3. **Hybrid**: Use free deployment + Cloudflare CDN for global performance
