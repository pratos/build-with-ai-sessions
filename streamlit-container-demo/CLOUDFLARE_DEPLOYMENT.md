# 🌐 Cloudflare Container Deployment Guide

Deploy your MCPs + Agents Demo to **Cloudflare Containers** for global, scalable, and secure hosting.

## 🚀 Why Cloudflare Containers?

- **Global Edge Deployment**: Automatically deployed to 320+ cities worldwide
- **Pay-per-Use**: Only pay when containers are actively running
- **Integrated Security**: Built-in DDoS protection and security features
- **Auto-scaling**: Scale from 0 to handle traffic spikes automatically
- **No Regional Configuration**: True "Region: Earth" deployment
- **Secure by Default**: Users must provide their own API keys

## 📋 Prerequisites

1. **Cloudflare Account**: Sign up at [cloudflare.com](https://cloudflare.com)
2. **Paid Workers Plan**: Containers require a paid plan ($5/month minimum)
3. **Docker**: For local container building
4. **Node.js & Wrangler CLI**: Latest version installed

```bash
npm install -g wrangler@latest
```

## 🛠️ Deployment Steps

### Step 1: Authenticate with Cloudflare

```bash
cd streamlit-container-demo
wrangler login
```

### Step 2: Verify Your Configuration

Check that your `wrangler.jsonc` has the correct settings:

```json
{
  "name": "mcp-agents-demo",
  "containers": [
    {
      "class_name": "StreamlitContainer",
      "image": "./Dockerfile",
      "max_instances": 10,
      "name": "streamlit-app",
      "instance_type": "basic"
    }
  ],
  "vars": {
    "ENVIRONMENT": "production"
  }
}
```

### Step 3: Deploy to Cloudflare

```bash
wrangler deploy
```

This command will:
1. Build your Docker container locally
2. Push the image to Cloudflare's registry
3. Deploy your Worker with container bindings
4. Provision containers globally across Cloudflare's edge

### Step 4: Check Deployment Status

```bash
# List your containers
wrangler containers list

# Check container images
wrangler containers images list
```

### Step 5: Access Your Application

Your app will be available at:
```
https://mcp-agents-demo.YOUR_SUBDOMAIN.workers.dev
```

## 🔒 Security Features

### Production Mode
When deployed, the app automatically enters **Production Mode**:
- ✅ No default API keys available
- ✅ Users must provide their own OpenAI and EXA API keys
- ✅ Keys are stored only in browser sessions (not on server)
- ✅ Built-in rate limiting (100 requests/minute per IP)
- ✅ Security headers automatically added

### API Key Management
- **Development**: Can use default keys or manual entry
- **Production**: Forces manual API key entry only
- **Client-Side Storage**: API keys never leave the user's browser
- **No Server Storage**: Keys are not logged or stored on Cloudflare

## 📊 Pricing

Cloudflare Containers pricing (as of 2025):

| Resource | Rate | Included (Workers Standard) |
|----------|------|---------------------------|
| **Memory** | $0.0000025 per GiB-second | 25 GiB-hours |
| **CPU** | $0.000020 per vCPU-second | 375 vCPU-minutes |
| **Disk** | $0.00000007 per GB-second | 200 GB-hours |

**Egress Pricing:**
- North America/Europe: $0.025/GB (1TB included)
- Other regions: $0.040-0.050/GB (500GB included)

### Cost Example
For a typical Streamlit app with moderate usage:
- **Basic instance**: 1 GiB memory, 1/4 vCPU
- **10 hours/month active**: ~$0.50-1.00/month
- **Scale to zero**: No charges when not in use

## 🔧 Configuration Options

### Instance Types Available

| Type | Memory | CPU | Disk | Use Case |
|------|--------|-----|------|----------|
| **dev** | 256 MiB | 1/16 vCPU | 2 GB | Testing |
| **basic** | 1 GiB | 1/4 vCPU | 4 GB | Production |
| **standard** | 4 GiB | 1/2 vCPU | 4 GB | Heavy workloads |

### Scaling Configuration

Update `wrangler.jsonc` for auto-scaling:

```json
{
  "containers": [
    {
      "class_name": "StreamlitContainer",
      "image": "./Dockerfile",
      "max_instances": 20,
      "instance_type": "standard",
      "autoscaling": {
        "minimum_instances": 1,
        "cpu_target": 75
      }
    }
  ]
}
```

## 🛠️ Troubleshooting

### Common Issues

**1. Authentication Error**
```bash
# Ensure you're logged in and have a paid plan
wrangler whoami
wrangler login
```

**2. Container Build Fails**
```bash
# Check Docker is running
docker info

# Test build locally
docker build -t test-streamlit .
```

**3. Container Won't Start**
```bash
# Check container logs
wrangler tail

# Verify health check endpoint
curl https://your-app.workers.dev/_stcore/health
```

**4. Slow First Load**
- First container start takes 30-60 seconds (cold start)
- Subsequent requests are much faster
- Consider keeping minimum instances > 0 for production

### Debug Commands

```bash
# View real-time logs
wrangler tail

# Check container status
wrangler containers list

# View deployment details
wrangler deployments list
```

## 🚀 Advanced Features

### Custom Domain

```bash
# Add custom domain
wrangler publish --compatibility-date 2025-01-01 --route "your-domain.com/*"
```

### Environment Variables

```bash
# Set secrets (for any sensitive config)
wrangler secret put SECRET_NAME
```

### Monitoring

- Built-in metrics in Cloudflare Dashboard
- Real-time logs via `wrangler tail`
- Container health monitoring
- Automatic error reporting

## 📈 Next Steps

1. **Monitor Usage**: Check Cloudflare Dashboard for metrics
2. **Scale Up**: Increase `max_instances` as needed
3. **Custom Domain**: Add your own domain for branding
4. **Enhanced Security**: Add additional rate limiting or auth
5. **CI/CD**: Set up GitHub Actions for automated deployments

## 🆘 Support

- **Cloudflare Docs**: [developers.cloudflare.com/containers](https://developers.cloudflare.com/containers)
- **Discord**: [Cloudflare Developers Discord](https://discord.gg/cloudflaredev)
- **GitHub Issues**: Report bugs in this repository

---

**🎉 Congratulations!** Your Streamlit app is now running globally on Cloudflare's edge network with enterprise-grade security and performance. 