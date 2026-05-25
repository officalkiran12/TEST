# SEO Configuration for FastAPI Backend

This document provides server-side SEO configurations for the Job Finder Portal.

## 1. HTTP HEADERS FOR SEO

Add these headers to your FastAPI app for better SEO:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add SEO-friendly HTTP headers
@app.middleware("http")
async def add_seo_headers(request, call_next):
    response = await call_next(request)
    
    # Cache control for static assets
    if request.url.path.startswith("/frontend"):
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    
    # Cache control for API responses
    elif request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutes
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # SEO headers
    response.headers["Vary"] = "Accept-Encoding"
    
    return response
```

## 2. CONTENT-TYPE HEADERS

Ensure proper content-type headers:

```python
@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return "User-agent: *\nAllow: /"

@app.get("/sitemap.xml", response_class=FileResponse)
async def sitemap():
    return FileResponse("sitemap.xml", media_type="application/xml")

@app.get("/", response_class=HTMLResponse)
async def home():
    return serve_nepal_portal()
```

## 3. GZIP COMPRESSION

Enable gzip compression for faster page loading:

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

## 4. STRUCTURED DATA VALIDATION

Validate JSON-LD with:
- Google Structured Data Testing Tool: https://search.google.com/structured-data/testing-tool
- Schema.org Validator: https://validator.schema.org/

## 5. PERFORMANCE OPTIMIZATION

### Image Optimization:
- Use WebP format for images
- Implement lazy loading
- Serve responsive images with srcset

```html
<img 
  src="image.jpg" 
  srcset="image-small.jpg 480w, image-medium.jpg 800w, image-large.jpg 1200w"
  sizes="(max-width: 480px) 480px, (max-width: 800px) 800px, 1200px"
  alt="Description" 
  loading="lazy"
>
```

### CSS/JavaScript Optimization:
- Minify CSS and JavaScript
- Defer non-critical JavaScript
- Use async for analytics scripts
- Inline critical CSS

```html
<link rel="preload" as="style" href="critical.css">
<script async src="analytics.js"></script>
<script defer src="non-critical.js"></script>
```

## 6. REDIRECTS FOR SEO

Implement 301 redirects for moved pages:

```python
@app.get("/old-url", status_code=301)
async def redirect_old_url(request: Request):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/new-url", status_code=301)
```

## 7. CANONICAL TAGS IN TEMPLATES

Include canonical tags to prevent duplicate content:

```html
<!-- Self-referential canonical -->
<link rel="canonical" href="https://yourdomain.com/current-page">

<!-- For paginated content -->
<link rel="prev" href="https://yourdomain.com/page/2">
<link rel="next" href="https://yourdomain.com/page/4">
```

## 8. BREADCRUMB NAVIGATION

Implement breadcrumb navigation for better UX and SEO:

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/jobs">Jobs</a></li>
    <li><a href="/jobs/tech">Tech Jobs</a></li>
    <li aria-current="page">Software Engineer</li>
  </ol>
</nav>
```

## 9. HREFLANG TAGS

Implement hreflang for multiple language versions:

```html
<!-- English version -->
<link rel="alternate" hreflang="en" href="https://yourdomain.com/">

<!-- Nepali version -->
<link rel="alternate" hreflang="ne" href="https://yourdomain.com/nepal">

<!-- Default/fallback -->
<link rel="alternate" hreflang="x-default" href="https://yourdomain.com/">
```

## 10. PAGINATION HANDLING

```html
<!-- First page -->
<link rel="first" href="/jobs?page=1">

<!-- Previous page -->
<link rel="prev" href="/jobs?page=2">

<!-- Next page -->
<link rel="next" href="/jobs?page=4">

<!-- Last page -->
<link rel="last" href="/jobs?page=10">
```

## 11. XML SITEMAP GENERATION

Generate dynamic sitemap for large sites:

```python
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring

@app.get("/sitemap-dynamic.xml", response_class=FileResponse)
async def dynamic_sitemap():
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add jobs dynamically
    jobs = get_all_jobs()  # Your function
    for job in jobs:
        url = SubElement(urlset, 'url')
        loc = SubElement(url, 'loc')
        loc.text = f"https://yourdomain.com/jobs/{job.id}"
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = job.updated_at.isoformat()
        priority = SubElement(url, 'priority')
        priority.text = "0.8"
    
    return Response(content=tostring(urlset), media_type="application/xml")
```

## 12. ROBOTS.TXT WITH DYNAMIC RULES

```python
@app.get("/robots.txt")
async def robots_txt():
    robots = """User-agent: *
Allow: /
Allow: /api/jobs
Allow: /frontend/
Allow: /docs

Disallow: /backend/
Disallow: /database/
Disallow: /admin/
Disallow: /temp/

User-agent: Googlebot
Allow: /
Crawl-delay: 0

User-agent: Bingbot
Allow: /
Crawl-delay: 0

Sitemap: https://yourdomain.com/sitemap.xml
Sitemap: https://yourdomain.com/sitemap-dynamic.xml

Crawl-delay: 1
Request-rate: 30/60
"""
    return Response(content=robots, media_type="text/plain")
```

## 13. SECURITY FOR SEO

### HTTPS (Production)
```
All SEO requires HTTPS in production
Use Let's Encrypt for free SSL certificates
```

### Security Headers
```python
response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
response.headers["Content-Security-Policy"] = "default-src 'self'"
response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
```

## 14. MONITORING & LOGGING

```python
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

## 15. PERFORMANCE MONITORING

### Key Metrics to Track:
- **Core Web Vitals**
  - Largest Contentful Paint (LCP): < 2.5s
  - First Input Delay (FID): < 100ms
  - Cumulative Layout Shift (CLS): < 0.1

- **Server Response Time**: < 200ms
- **Page Load Time**: < 3s
- **TTFB (Time to First Byte)**: < 600ms

### Tools:
- Google PageSpeed Insights
- GTmetrix
- WebPageTest
- Lighthouse CLI

---

## IMPLEMENTATION CHECKLIST

- [ ] Add HTTP headers middleware
- [ ] Enable Gzip compression
- [ ] Implement 301 redirects
- [ ] Validate JSON-LD schemas
- [ ] Optimize images
- [ ] Minify CSS/JavaScript
- [ ] Add canonical tags
- [ ] Implement breadcrumbs
- [ ] Setup hreflang tags
- [ ] Generate dynamic sitemap
- [ ] Implement robots.txt
- [ ] Add security headers
- [ ] Setup monitoring
- [ ] Test with Google tools
- [ ] Monitor Core Web Vitals

---

**Version**: 1.0
**Last Updated**: May 24, 2026
