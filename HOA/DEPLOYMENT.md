# 🚀 ÇORLU LİHKAB - Complete Deployment & Performance Guide

## 📊 Performance Summary

### Current Optimizations (Active)
```
✅ GZIP Compression (70% boyut azaltma)
✅ Browser Caching (1yr static, 1hr HTML)
✅ Security Headers (MIME, XSS, Clickjacking protection)
✅ Script Defer Loading (non-blocking JS)
✅ DNS Prefetch & Preconnect (faster external requests)
✅ Font Display: Swap (FOIT prevention)
✅ Critical CSS Preload (faster rendering)
```

### Performance Metrics
```
Static Assets:     ~25KB (gzip'd)
HTML Response:     ~10KB (gzip'd)
Total Page Size:   ~50KB (all assets gzip'd)

First Load:        ~2-3 seconds
Repeat Visit:      <500ms (browser cache)
```

---

## 🌐 Deployment Options

### Option 1: Render.com (Recommended for Beginners)

**Advantages:**
- ✅ Free tier available
- ✅ Auto HTTPS/SSL
- ✅ Built-in Nginx caching
- ✅ Auto-deploy from GitHub
- ✅ No server management

**Steps:**
```bash
1. Push code to GitHub
2. Sign up at render.com
3. New Web Service → Connect GitHub
4. Settings:
   - Build Command: pip install -r requirements.txt
   - Start Command: gunicorn app:app
   - Environment: Python
5. Deploy
```

**Performance Notes:**
- Render has built-in optimization
- No extra .htaccess or nginx.conf needed
- Just deploy and it works

---

### Option 2: Heroku

**Advantages:**
- ✅ Easy deployment
- ✅ Good for rapid development
- ⚠️  Costs money (after free tier)

**Steps:**
```bash
1. Create Procfile (already done):
   web: gunicorn app:app

2. Deploy:
   heroku login
   heroku create corlulihkab
   git push heroku main
```

---

### Option 3: Custom VPS (DigitalOcean/AWS/Linode)

**Advantages:**
- ✅ Full control
- ✅ Better performance
- ✅ Custom configurations
- ⚠️  Server management required

**Setup:**

```bash
# 1. SSH ke server
ssh root@your_server_ip

# 2. Update system
apt update && apt upgrade -y

# 3. Install Python & dependencies
apt install python3 python3-pip python3-venv git nginx -y

# 4. Clone application
cd /var/www
git clone https://github.com/yourusername/corlulihkab.git
cd corlulihkab

# 5. Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 6. Gunicorn setup
pip install gunicorn

# 7. Create systemd service
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=Gunicorn service for ÇORLU LİHKAB
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/corlulihkab
ExecStart=/var/www/corlulihkab/venv/bin/gunicorn \\
    --workers 4 \\
    --worker-class sync \\
    --bind 0.0.0.0:8000 \\
    app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 8. Enable Gunicorn
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# 9. Setup Nginx
sudo cp nginx.conf /etc/nginx/sites-available/corlulihkab
sudo ln -s /etc/nginx/sites-available/corlulihkab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 10. SSL Certificate (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx -y
sudo certbot certonly --nginx -d www.corlulihkab.com -d corlulihkab.com

# 11. Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# 12. Done!
echo "Deployment complete!"
```

**Monitoring:**
```bash
# Check Gunicorn status
sudo systemctl status gunicorn

# View logs
sudo journalctl -u gunicorn -f

# Restart Gunicorn (after code changes)
sudo systemctl restart gunicorn

# Check Nginx
sudo systemctl status nginx
```

---

## 📈 Next Performance Improvements

### 1. Image Optimization (HIGH PRIORITY)
```bash
# Convert images to WebP
for img in static/img/*.png; do
    cwebp "$img" -o "${img%.png}.webp"
done

# In HTML templates:
<picture>
    <source srcset="image.webp" type="image/webp">
    <img src="image.png" alt="..." loading="lazy">
</picture>
```

### 2. CSS/JS Minification (MEDIUM PRIORITY)
```bash
# Install tools
npm install -g csso-cli uglify-js

# Minify CSS
csso static/css/style.css -o static/css/style.min.css

# Minify JS
uglifyjs static/js/slider.js -o static/js/slider.min.js

# Update references in base.html:
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.min.css') }}">
<script src="{{ url_for('static', filename='js/slider.min.js') }}" defer></script>
```

### 3. CDN Setup with Cloudflare (MEDIUM PRIORITY)

```
1. Sign up at cloudflare.com
2. Add your domain
3. Update nameservers
4. Enable:
   - Automatic compression
   - Caching
   - DDoS protection
5. Performance: +50% faster globally
```

### 4. Inline Critical CSS (ADVANCED)
```bash
npm install --save-dev critical

critical src/templates/base.html \
  --width 1200 --height 800 \
  --minify \
  --output inline-css.html
```

---

## 🔍 Testing & Monitoring

### Google PageSpeed Insights
```
https://pagespeed.web.dev/
→ Enter: https://www.corlulihkab.com
→ View Core Web Vitals
```

### Lighthouse (Chrome DevTools)
```
1. Open DevTools (F12)
2. Lighthouse tab
3. Analyze page load
4. View recommendations
```

### GTmetrix Performance Testing
```
https://gtmetrix.com/
→ Detailed waterfall analysis
→ Optimization recommendations
```

### Uptime Monitoring
```bash
# Using UptimeRobot (free)
https://uptimerobot.com/
- Monitor site availability
- Get alerts if down
- 5-minute check interval
```

---

## 🔐 Security Checklist

- [x] HTTPS (Let's Encrypt SSL)
- [x] Security headers (X-Content-Type-Options, X-Frame-Options, etc)
- [x] GZIP compression
- [x] Input validation (Flask)
- [ ] Rate limiting (TODO - add Flask-Limiter)
- [ ] WAF rules (TODO - Cloudflare)
- [ ] Database hardening (N/A - static site)
- [ ] Regular backups (TODO - GitHub backups)

---

## 📋 Maintenance

### Daily
- Monitor error logs
- Check uptime status

### Weekly
- Review Google Analytics
- Check security alerts

### Monthly
- Update dependencies: `pip list --outdated`
- Update OS: `apt update && apt upgrade`
- SSL certificate check: `certbot renew --dry-run`
- Backup code: `git push` (GitHub backup)

### Quarterly
- Performance audit
- SEO audit
- Security audit

---

## 📞 Troubleshooting

### App not responding
```bash
# Check Gunicorn
sudo systemctl status gunicorn

# Restart
sudo systemctl restart gunicorn

# View logs
sudo journalctl -u gunicorn -n 100
```

### High memory usage
```bash
# Reduce Gunicorn workers
# Edit /etc/systemd/system/gunicorn.service
# Change: --workers 4 → --workers 2
sudo systemctl restart gunicorn
```

### SSL certificate issue
```bash
# Renew certificate
sudo certbot renew --force-renewal

# Check expiry
sudo certbot certificates
```

### Site slow
```bash
# Check cache headers
curl -I https://www.corlulihkab.com

# Verify gzip
curl -H "Accept-Encoding: gzip" https://www.corlulihkab.com -o /dev/null -w '%{size_download}'

# Run PageSpeed
https://pagespeed.web.dev/
```

---

## 🎯 Key Deployment Decision Tree

```
Where to deploy?

├─ Want simplest setup?
│  └─ Use Render.com ✅ (recommended)
│
├─ Want more control?
│  └─ Custom VPS (nginx.conf provided)
│
├─ Want AWS/enterprise?
│  └─ AWS Elastic Beanstalk
│
└─ Want serverless?
   └─ AWS Lambda + API Gateway (need refactor)
```

---

## 📚 Useful Resources

### Performance
- [Web.dev Performance Guide](https://web.dev/performance/)
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [MDN: Web Performance](https://developer.mozilla.org/en-US/docs/Web/Performance)

### Deployment
- [Render Docs](https://render.com/docs)
- [Heroku Docs](https://devcenter.heroku.com/)
- [Nginx Docs](https://nginx.org/en/docs/)

### Security
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Cloudflare Security](https://www.cloudflare.com/)

---

**Last Updated:** 2026-02-05
**Version:** 1.1.0
