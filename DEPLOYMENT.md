# Deployment Guide

This guide provides step-by-step instructions for deploying the Universal Video Downloader Web App in production environments.

## Quick Start (Development)

### Automated Setup
```bash
# Clone the repository
git clone https://github.com/your-username/video.git
cd video

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Manual Setup

#### Backend Setup
```bash
cd video_downloader_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
python src/main.py --init-db
```

#### Frontend Setup
```bash
cd video-downloader-frontend
npm install
npm run build
cp -r dist/* ../video_downloader_backend/src/static/
```

#### Start Application
```bash
cd video_downloader_backend
source venv/bin/activate
python src/main.py
```

Access at: http://localhost:5000

## Production Deployment

### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.8+
- Node.js 16+
- Nginx (recommended)
- PostgreSQL (recommended for production)
- SSL certificate (Let's Encrypt recommended)

### Step 1: Server Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nodejs npm nginx postgresql postgresql-contrib

# Install certbot for SSL
sudo apt install -y certbot python3-certbot-nginx
```

### Step 2: Application Setup

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/your-username/video.git
sudo chown -R $USER:$USER video
cd video

# Setup backend
cd video_downloader_backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server

# Configure environment
cp .env.example .env
nano .env  # Edit with production settings
```

### Step 3: Database Configuration

```bash
# Create PostgreSQL database
sudo -u postgres psql
```

In PostgreSQL:
```sql
CREATE DATABASE video_downloader;
CREATE USER video_app WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE video_downloader TO video_app;
\q
```

Update `.env`:
```bash
DATABASE_URL=postgresql://video_app:your_secure_password@localhost/video_downloader
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-generated-secret-key
```

Initialize database:
```bash
python src/main.py --init-db
```

### Step 4: Build Frontend

```bash
cd ../video-downloader-frontend
npm install
npm run build
cp -r dist/* ../video_downloader_backend/src/static/
```

### Step 5: Systemd Service

Create `/etc/systemd/system/video-downloader.service`:

```ini
[Unit]
Description=Universal Video Downloader Web App
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/video/video_downloader_backend
Environment="PATH=/opt/video/video_downloader_backend/venv/bin"
EnvironmentFile=/opt/video/video_downloader_backend/.env
ExecStart=/opt/video/video_downloader_backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 --worker-class eventlet -w 1 src.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl enable video-downloader
sudo systemctl start video-downloader
sudo systemctl status video-downloader
```

### Step 6: Nginx Configuration

Create `/etc/nginx/sites-available/video-downloader`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL configuration (after running certbot)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # File upload size
    client_max_body_size 100M;
    
    # Proxy settings
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # WebSocket support
    location /socket.io/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and configure SSL:
```bash
sudo ln -s /etc/nginx/sites-available/video-downloader /etc/nginx/sites-enabled/
sudo nginx -t
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
sudo systemctl restart nginx
```

### Step 7: Google Drive API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Drive API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `https://yourdomain.com/api/auth/google-drive/callback`
6. Update `.env` with credentials
7. Restart service: `sudo systemctl restart video-downloader`

### Step 8: Firewall Configuration

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

## Monitoring and Maintenance

### View Logs
```bash
# Application logs
sudo journalctl -u video-downloader -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Update Application
```bash
cd /opt/video
sudo git pull
cd video_downloader_backend
source venv/bin/activate
pip install -r requirements.txt
cd ../video-downloader-frontend
npm install
npm run build
cp -r dist/* ../video_downloader_backend/src/static/
sudo systemctl restart video-downloader
```

### Database Backup
```bash
# Create backup
pg_dump -U video_app video_downloader > backup_$(date +%Y%m%d).sql

# Restore backup
psql -U video_app video_downloader < backup_20231201.sql
```

### Performance Tuning

#### PostgreSQL
Edit `/etc/postgresql/*/main/postgresql.conf`:
```
shared_buffers = 256MB
work_mem = 16MB
maintenance_work_mem = 128MB
effective_cache_size = 1GB
max_connections = 100
```

#### Nginx Cache
Add to server block:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
proxy_cache my_cache;
```

## Troubleshooting

### Application Won't Start
```bash
# Check service status
sudo systemctl status video-downloader

# Check logs
sudo journalctl -u video-downloader -n 50

# Check if port is in use
sudo netstat -tulpn | grep 5000
```

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -U video_app -d video_downloader -h localhost
```

### Permission Issues
```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/video
sudo chmod -R 755 /opt/video
```

### SSL Certificate Renewal
```bash
# Test renewal
sudo certbot renew --dry-run

# Renew (automatic via cron)
sudo certbot renew
```

## Security Best Practices

1. **Regular Updates**: Keep system and dependencies updated
2. **Strong Passwords**: Use strong, unique passwords for database
3. **Limited Access**: Restrict SSH access to specific IPs
4. **Backup Strategy**: Regular automated backups
5. **Monitor Logs**: Set up log monitoring and alerting
6. **Rate Limiting**: Implement rate limiting in Nginx
7. **Fail2ban**: Install and configure fail2ban for SSH protection

## Scaling Considerations

### Horizontal Scaling
- Use Redis for shared queue management
- Deploy multiple application instances behind load balancer
- Use shared file storage (NFS, S3, etc.)

### Vertical Scaling
- Increase worker processes in gunicorn
- Optimize PostgreSQL configuration
- Add more RAM/CPU as needed

### CDN Integration
- Use Cloudflare or similar for static assets
- Reduce bandwidth usage
- Improve global performance

## Support

For issues and questions:
- Check documentation: `/Universal_Video_Downloader_Documentation.md`
- Review logs: `sudo journalctl -u video-downloader`
- GitHub Issues: https://github.com/your-username/video/issues
