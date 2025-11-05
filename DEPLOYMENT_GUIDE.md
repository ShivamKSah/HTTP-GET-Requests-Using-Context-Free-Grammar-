# 🚀 **CFG QODER - Production Deployment Guide**

## 📋 **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Docker Deployment](#docker-deployment)
3. [Environment Configuration](#environment-configuration)
4. [Security Setup](#security-setup)
5. [Monitoring & Logging](#monitoring--logging)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 **Prerequisites**

### **System Requirements**
- **Docker Engine** 20.10+ with Docker Compose V2
- **Memory**: Minimum 2GB RAM (4GB recommended)
- **Storage**: 5GB free space
- **CPU**: 2+ cores recommended
- **Operating System**: Linux, macOS, or Windows with WSL2

### **Network Requirements**
- **Port 80**: Frontend (HTTP)
- **Port 443**: HTTPS (if SSL configured)
- **Port 5000**: Backend API (internal)
- **Port 6379**: Redis (internal)
- **Port 9090**: Prometheus monitoring (optional)

---

## 🐳 **Docker Deployment**

### **Quick Start Production Deployment**

#### **Step 1: Clone and Prepare**
```bash
# Clone the repository
git clone <your-repo-url> cfg-qoder
cd cfg-qoder

# Create production configuration
cp backend/config.example.yaml backend/config.yaml
```

#### **Step 2: Configure Environment**
Create `.env` file in project root:
```bash
# Production Environment Variables
CFG_QODER_ENV=production
SECRET_KEY=your-super-secure-secret-key-change-this
DATABASE_URL=sqlite:///cfg_validator.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=http://your-domain.com,https://your-domain.com

# Security Settings
ENABLE_RATE_LIMITING=true
MAX_REQUEST_SIZE=16777216
ENABLE_METRICS=true

# Logging Configuration
LOG_LEVEL=WARNING
ENABLE_FILE_LOGGING=true
LOG_DIR=/app/logs

# NLP Configuration
ENABLE_NLP_SUMMARIZATION=true
ENABLE_NLP_CLASSIFICATION=true
MAX_TEXT_LENGTH=50000
```

#### **Step 3: Deploy with Docker Compose**
```bash
# Start all services in production mode
docker-compose -f docker-compose.prod.yml up -d

# Check service status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

#### **Step 4: Verify Deployment**
```bash
# Test backend health
curl http://localhost:5000/api/health

# Test frontend
curl http://localhost/

# Test full validation workflow
curl -X POST http://localhost/api/validate \
  -H "Content-Type: application/json" \
  -d '{"request_line": "GET /test HTTP/1.1"}'
```

### **Advanced Production Setup**

#### **SSL/HTTPS Configuration**
Create `nginx-ssl.conf`:
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/ssl/certs/your-cert.pem;
    ssl_certificate_key /etc/ssl/private/your-key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    
    # ... rest of configuration
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

#### **Load Balancer Configuration**
```yaml
# docker-compose.loadbalanced.yml
version: '3.8'
services:
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/ssl:ro
    depends_on:
      - backend-1
      - backend-2
    networks:
      - cfg-qoder-network

  backend-1:
    build: ./backend
    expose:
      - "5000"
    environment:
      - CFG_QODER_ENV=production
    networks:
      - cfg-qoder-network

  backend-2:
    build: ./backend
    expose:
      - "5000"
    environment:
      - CFG_QODER_ENV=production
    networks:
      - cfg-qoder-network
```

---

## ⚙️ **Environment Configuration**

### **Production Configuration File**
Create `backend/config.yaml`:
```yaml
environment: production

database:
  url: "sqlite:///cfg_validator.db"
  echo: false
  pool_size: 10
  max_overflow: 20

api:
  host: "0.0.0.0"
  port: 5000
  debug: false
  secret_key: "${SECRET_KEY}"
  max_content_length: 16777216
  cors_origins:
    - "https://your-domain.com"
    - "https://www.your-domain.com"

logging:
  level: "WARNING"
  enable_console: false
  enable_file: true
  log_dir: "/app/logs"
  max_file_size: 10485760
  backup_count: 5

security:
  enable_rate_limiting: true
  enable_input_validation: true
  enable_sanitization: true
  max_request_size: 16777216
  enable_cors: true
  enable_csrf_protection: true

performance:
  enable_metrics: true
  enable_caching: true
  cache_timeout: 300
  max_cache_size: 1000

nlp:
  enable_summarization: true
  enable_classification: true
  enable_query_processing: true
  max_text_length: 50000
  cache_enabled: true
  cache_ttl: 3600

automata:
  enable_nfa: true
  enable_dfa: true
  enable_regex_matching: true
  max_pattern_length: 1000
  timeout_seconds: 30
  performance_monitoring: true
```

### **Environment Variables Reference**
```bash
# Core Configuration
CFG_QODER_ENV=production|staging|development
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=sqlite:///cfg_validator.db
DATABASE_ECHO=false

# API Settings
API_HOST=0.0.0.0
API_PORT=5000
API_DEBUG=false
CORS_ORIGINS=https://domain1.com,https://domain2.com

# Security
ENABLE_RATE_LIMITING=true
ENABLE_INPUT_VALIDATION=true
MAX_REQUEST_SIZE=16777216

# Logging
LOG_LEVEL=WARNING|ERROR|INFO|DEBUG
ENABLE_CONSOLE_LOGGING=false
ENABLE_FILE_LOGGING=true
LOG_DIR=/app/logs

# Features
ENABLE_NLP_SUMMARIZATION=true
ENABLE_NLP_CLASSIFICATION=true
ENABLE_METRICS=true
ENABLE_CACHING=true

# Performance
MAX_TEXT_LENGTH=50000
CACHE_TTL=3600
SLOW_QUERY_THRESHOLD=1.0
```

---

## 🔒 **Security Setup**

### **Production Security Checklist**

#### **✅ Essential Security Measures**
- [x] **Rate Limiting**: Enabled with IP-based throttling
- [x] **Input Validation**: Comprehensive sanitization
- [x] **Security Headers**: HTTPS, CSP, HSTS, X-Frame-Options
- [x] **CORS Configuration**: Restricted to allowed origins
- [x] **Request Size Limits**: 16MB maximum
- [x] **Error Handling**: No sensitive information exposed

#### **🔒 Advanced Security Configuration**
```python
# In production app.py
from security_validation import SecurityMiddleware, init_security

app = Flask(__name__)
security_middleware, audit_logger = init_security(app)

# Configure security settings
app.config.update({
    'SECRET_KEY': os.environ.get('SECRET_KEY'),
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,
    'SECURITY_HEADERS': {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self'",
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    }
})
```

#### **🚨 Security Monitoring**
```bash
# Monitor security events
curl http://localhost:5000/api/security/stats

# Check audit logs
curl http://localhost:5000/api/security/audit

# View rate limiting status
curl -I http://localhost:5000/api/validate
# Check headers: X-RateLimit-Limit, X-RateLimit-Remaining
```

### **Firewall Configuration**
```bash
# Ubuntu/Debian UFW
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw deny 5000/tcp   # Block direct backend access
sudo ufw enable

# CentOS/RHEL Firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 📊 **Monitoring & Logging**

### **Log Management**
```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs backend -f

# View specific log files
docker exec cfg-qoder-backend tail -f /app/logs/cfg_qoder.log
docker exec cfg-qoder-backend tail -f /app/logs/cfg_qoder_errors.log
docker exec cfg-qoder-backend tail -f /app/logs/cfg_qoder_performance.log
```

### **Health Monitoring**
```bash
# Backend health check
curl http://localhost:5000/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-20T15:30:00Z",
  "version": "2.0.0",
  "uptime": "2 hours, 45 minutes",
  "components": {
    "database": "healthy",
    "logging": "healthy",
    "nlp": "healthy",
    "automata": "healthy"
  }
}
```

### **Performance Metrics**
```bash
# Get system statistics
curl http://localhost:5000/api/stats/summary

# Analytics overview
curl http://localhost:5000/api/analytics?days=7

# Security statistics
curl http://localhost:5000/api/security/stats
```

### **Prometheus Monitoring**
Create `monitoring/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  # - "first_rules.yml"

scrape_configs:
  - job_name: 'cfg-qoder-backend'
    static_configs:
      - targets: ['backend:5000']
    metrics_path: '/api/metrics'
    scrape_interval: 30s

  - job_name: 'cfg-qoder-frontend'
    static_configs:
      - targets: ['frontend:80']
    scrape_interval: 60s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          # - alertmanager:9093
```

---

## ⚡ **Performance Optimization**

### **Production Optimization Settings**

#### **Backend Optimization**
```yaml
# config.yaml - Performance section
performance:
  enable_metrics: true
  enable_profiling: false  # Disable in production
  slow_query_threshold: 1.0
  enable_caching: true
  cache_timeout: 300
  max_cache_size: 1000

# Enable request pooling
api:
  pool_size: 10
  max_overflow: 20
  pool_timeout: 30
  pool_recycle: 3600
```

#### **Frontend Optimization**
```nginx
# nginx.conf optimizations
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/javascript
    application/json;

# Cache static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# Enable HTTP/2
listen 443 ssl http2;
```

#### **Database Optimization**
```bash
# SQLite optimization for production
echo "PRAGMA journal_mode = WAL;" | sqlite3 cfg_validator.db
echo "PRAGMA synchronous = NORMAL;" | sqlite3 cfg_validator.db
echo "PRAGMA cache_size = 10000;" | sqlite3 cfg_validator.db
echo "PRAGMA temp_store = memory;" | sqlite3 cfg_validator.db
```

### **Scaling Configuration**
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  backend:
    build: ./backend
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    environment:
      - CFG_QODER_ENV=production

  frontend:
    build: ./frontend
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.25'
          memory: 128M
```

---

## 🔧 **Troubleshooting**

### **Common Issues and Solutions**

#### **Issue 1: Backend Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Common causes:
# 1. Missing environment variables
# 2. Port conflicts
# 3. Permission issues with logs directory

# Solutions:
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --force-recreate
```

#### **Issue 2: High Memory Usage**
```bash
# Monitor resource usage
docker stats

# Optimize configuration
# Reduce cache sizes in config.yaml:
performance:
  max_cache_size: 500  # Reduce from 1000
  cache_timeout: 180   # Reduce from 300

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

#### **Issue 3: Rate Limiting Too Aggressive**
```bash
# Check current limits
curl -I http://localhost:5000/api/validate

# Adjust in config.yaml:
security:
  rate_limit_default: "1000/hour"  # Increase from 100/hour

# Or via environment:
export RATE_LIMIT_DEFAULT="1000/hour"
```

#### **Issue 4: SSL Certificate Problems**
```bash
# Check certificate validity
openssl x509 -in /path/to/cert.pem -text -noout

# Update nginx SSL config
# Ensure paths are correct in docker-compose.yml:
volumes:
  - ./ssl/cert.pem:/etc/ssl/certs/cert.pem:ro
  - ./ssl/key.pem:/etc/ssl/private/key.pem:ro
```

### **Performance Troubleshooting**
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/api/health

# Create curl-format.txt:
echo "time_namelookup:  %{time_namelookup}\ntime_connect:     %{time_connect}\ntime_appconnect:  %{time_appconnect}\ntime_pretransfer: %{time_pretransfer}\ntime_redirect:    %{time_redirect}\ntime_starttransfer: %{time_starttransfer}\ntime_total:       %{time_total}\n" > curl-format.txt

# Monitor database performance
docker exec cfg-qoder-backend sqlite3 cfg_validator.db ".schema"
docker exec cfg-qoder-backend sqlite3 cfg_validator.db "EXPLAIN QUERY PLAN SELECT * FROM request_logs LIMIT 10;"
```

### **Log Analysis**
```bash
# Analyze error patterns
docker exec cfg-qoder-backend grep "ERROR" /app/logs/cfg_qoder_errors.log | tail -20

# Check performance bottlenecks
docker exec cfg-qoder-backend grep "slow_query" /app/logs/cfg_qoder_performance.log

# Monitor rate limiting
docker exec cfg-qoder-backend grep "rate_limit" /app/logs/cfg_qoder_api.log | tail -10
```

---

## 🚀 **Production Deployment Commands**

### **Complete Deployment Script**
```bash
#!/bin/bash
# deploy.sh - Complete production deployment

set -e

echo "🚀 Starting CFG QODER production deployment..."

# Step 1: Prepare environment
echo "📋 Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed. Aborting." >&2; exit 1; }

# Step 2: Stop existing services
echo "⏹️ Stopping existing services..."
docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

# Step 3: Build and start services
echo "🔨 Building and starting services..."
docker-compose -f docker-compose.prod.yml up -d --build

# Step 4: Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Step 5: Health checks
echo "🏥 Performing health checks..."
if curl -f http://localhost:5000/api/health > /dev/null 2>&1; then
    echo "✅ Backend health check passed"
else
    echo "❌ Backend health check failed"
    exit 1
fi

if curl -f http://localhost/ > /dev/null 2>&1; then
    echo "✅ Frontend health check passed"
else
    echo "❌ Frontend health check failed"
    exit 1
fi

# Step 6: Display status
echo "📊 Deployment status:"
docker-compose -f docker-compose.prod.yml ps

echo "🎉 CFG QODER deployed successfully!"
echo "🌐 Frontend: http://localhost/"
echo "🔧 Backend API: http://localhost:5000/api/"
echo "📊 Monitoring: http://localhost:9090/ (if enabled)"
```

### **Maintenance Commands**
```bash
# Update deployment
./deploy.sh

# View service status
docker-compose -f docker-compose.prod.yml ps

# Restart specific service
docker-compose -f docker-compose.prod.yml restart backend

# View logs
docker-compose -f docker-compose.prod.yml logs -f --tail=100

# Backup database
docker exec cfg-qoder-backend cp /app/cfg_validator.db /app/logs/backup-$(date +%Y%m%d).db

# Update SSL certificates
docker-compose -f docker-compose.prod.yml restart frontend

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

---

## 🎯 **Final Production Checklist**

### **Pre-Deployment** ✅
- [ ] Environment variables configured
- [ ] SSL certificates obtained and installed
- [ ] Firewall rules configured
- [ ] DNS records pointed to server
- [ ] Backup strategy implemented

### **Security** 🔒
- [ ] Rate limiting enabled and tested
- [ ] Security headers configured
- [ ] Input validation active
- [ ] HTTPS enforced
- [ ] Sensitive data encrypted

### **Performance** ⚡
- [ ] Caching enabled
- [ ] Database optimized
- [ ] Static asset compression
- [ ] Load balancing configured (if needed)
- [ ] Resource limits set

### **Monitoring** 📊
- [ ] Health checks working
- [ ] Log aggregation setup
- [ ] Metrics collection active
- [ ] Alerting configured
- [ ] Backup monitoring

### **Documentation** 📚
- [ ] Deployment procedures documented
- [ ] Runbook created
- [ ] Emergency contacts established
- [ ] Rollback procedures tested

**🎉 Your CFG QODER production deployment is complete and secure!**