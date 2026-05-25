/**
 * ==========================================================================
 * NATIONAL JOB PORTAL — CORE ENGINE
 * ==========================================================================
 */
const API_BASE = "http://127.0.0.1:8000/api";

document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Menu Drawer Toggle
    setupMobileMenu();

    // 2. Sticky Navbar state scroll handler
    const navbar = document.querySelector(".navbar");
    window.addEventListener("scroll", () => {
        if (window.scrollY > 20) {
            navbar.style.background = "rgba(7, 10, 19, 0.95)";
            navbar.style.padding = "0.7rem 2rem";
        } else {
            navbar.style.background = "rgba(7, 10, 19, 0.75)";
            navbar.style.padding = "1rem 2rem";
        }
    });

    // 3. Page specific bootstrapping triggers
    const path = window.location.pathname;
    if (path.endsWith("index.html") || path === "/" || path === "/global" || path.endsWith("job%20finder/") || path.endsWith("job finder/")) {
        bootstrapHomepage();
    }
});

// Setup Mobile Menu Drawer Interaction
function setupMobileMenu() {
    const toggle = document.querySelector(".menu-toggle");
    const navLinks = document.querySelector(".nav-links");
    if (toggle && navLinks) {
        toggle.addEventListener("click", () => {
            navLinks.style.display = navLinks.style.display === "flex" ? "none" : "flex";
            if (navLinks.style.display === "flex") {
                navLinks.style.flexDirection = "column";
                navLinks.style.position = "absolute";
                navLinks.style.top = "100%";
                navLinks.style.left = "0";
                navLinks.style.width = "100%";
                navLinks.style.background = "#0b0f19";
                navLinks.style.padding = "1.5rem";
                navLinks.style.borderBottom = "1px solid rgba(255, 255, 255, 0.08)";
            }
        });
    }
}

// Generate Premium Job Card HTML Components
function createJobCardMarkup(job) {
    const isSaved = SavedJobsManager.isSaved(job.id);
    const saveIcon = isSaved 
        ? `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #f43f5e;"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>`
        : `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>`;
        
    const saveClass = isSaved ? "bookmark-btn saved" : "bookmark-btn";
    
    // Skills tags
    const skillsArray = job.skills ? job.skills.split(",") : ["Tech"];
    const skillsHtml = skillsArray.slice(0, 4).map(skill => `<span class="skill-tag">${skill.trim()}</span>`).join("");
    
    // Format date string beautifully (e.g. "2 days ago")
    const dateFormatted = timeAgo(job.posted_date);
    
    // Determine logo source: use http(s) URLs, else fallback to initials
    const initials = job.company_name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
    const actualLogo = job.company_logo && job.company_logo.startsWith("http") ? job.company_logo : null;

    // Correct details link depending on current folder structure
    const detailsUrl = window.location.pathname.includes("pages/") 
        ? `details.html?id=${job.id}` 
        : `frontend/pages/details.html?id=${job.id}`;

    return `
        <div class="job-card" id="job-card-${job.id}">
            <div>
                <div class="job-card-header">
                    ${actualLogo
                        ? `<img class="company-logo" src="${actualLogo}" onerror="this.onerror=null;imgFallback(this,'${initials}')" alt="${job.company_name} logo" loading="lazy">`
                        : `<div class="company-logo company-logo-init">${initials}</div>`
                    }
                    <button class="${saveClass}" onclick='event.stopPropagation(); SavedJobsManager.toggleSave(${JSON.stringify(job).replace(/'/g, "&apos;")}, this)'>
                        ${saveIcon}
                    </button>
                </div>
                
                <div class="job-info" onclick="window.location.href='${detailsUrl}'" style="cursor: pointer;">
                    <div class="company-name">${job.company_name}</div>
                    <h3 class="job-title">${job.title}</h3>
                    
                    <div class="badge-row">
                        ${job.is_remote ? '<span class="badge badge-remote">Remote</span>' : ''}
                        ${job.visa_sponsorship ? '<span class="badge badge-visa">Visa Sponsored</span>' : ''}
                        <span class="badge badge-location">${job.location}</span>
                    </div>
                    
                    <div class="skills-row">
                        ${skillsHtml}
                    </div>
                </div>
            </div>
            
            <div class="job-card-footer">
                <div>
                    <div class="job-salary">${job.salary || "Not specified"}</div>
                    <div class="job-date">${dateFormatted}</div>
                </div>
                <a href="${getApplyUrl(job)}" target="_blank" rel="noopener noreferrer" class="btn-card-apply">Apply Now</a>
            </div>
        </div>
    `;
}

// Compute Time-Ago text dynamically
function timeAgo(dateString) {
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffMs = now - date;
        
        const diffMins = Math.floor(diffMs / 1000 / 60);
        if (diffMins < 60) return `${diffMins}m ago`;
        
        const diffHrs = Math.floor(diffMins / 60);
        if (diffHrs < 24) return `${diffHrs}h ago`;
        
        const diffDays = Math.floor(diffHrs / 24);
        if (diffDays === 1) return `Yesterday`;
        return `${diffDays}d ago`;
    } catch (e) {
        return "Recently";
    }
}

// Render Skeleton cards during fetches to wow the user with instant fluid states
function getSkeletonCardsMarkup(count = 6) {
    let html = "";
    for (let i = 0; i < count; i++) {
        html += `
            <div class="skeleton-card">
                <div>
                    <div class="skeleton-text skeleton-logo"></div>
                    <div class="skeleton-text skeleton-title"></div>
                    <div class="skeleton-text skeleton-company"></div>
                    <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                        <div class="skeleton-text skeleton-badge"></div>
                        <div class="skeleton-text skeleton-badge"></div>
                    </div>
                    <div class="skeleton-text skeleton-skills"></div>
                </div>
                <div class="skeleton-footer">
                    <div class="skeleton-text" style="height: 16px; width: 40%;"></div>
                </div>
            </div>
        `;
    }
    return html;
}

// Bootstrapping index.html Home Feed
async function bootstrapHomepage() {
    const latestGrid = document.getElementById("homepage-latest-jobs-grid");
    if (latestGrid) {
        latestGrid.innerHTML = getSkeletonCardsMarkup(6);
    }

    try {
        // 1. Fetch Latest Jobs Feed
        const jobsRes = await fetch(`${API_BASE}/latest?limit=6`);
        if (jobsRes.status === 200) {
            const jobs = await jobsRes.json();
            if (latestGrid) {
                if (jobs.length === 0) {
                    latestGrid.innerHTML = `
                        <div class="empty-state" style="grid-column: 1 / -1;">
                            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
                            <h3>No active jobs compiled</h3>
                            <p>Scraping threads are loading listings right now. Please refresh in a moment.</p>
                        </div>
                    `;
                } else {
                    latestGrid.innerHTML = jobs.map(job => createJobCardMarkup(job)).join("");
                }
            }
        }

        // 2. Fetch Trending Metrics
        const trendRes = await fetch(`${API_BASE}/trending`);
        if (trendRes.status === 200) {
            const data = await trendRes.json();
            
            // Populating trending search tag links
            const tagsWrapper = document.getElementById("trending-tags-row");
            if (tagsWrapper && data.trending_tags) {
                tagsWrapper.innerHTML = data.trending_tags.map(item => `
                    <span class="quick-tag" onclick="quickSearchTag('${item.tag}')">${item.tag} (${item.count})</span>
                `).join("");
            }
        }

        // 3. Fetch Country Filter Aggregates
        const countryRes = await fetch(`${API_BASE}/countries`);
        if (countryRes.status === 200) {
            const countries = await countryRes.json();
            const countryGrid = document.getElementById("homepage-country-grid");
            if (countryGrid && countries) {
                countryGrid.innerHTML = countries.slice(0, 4).map(c => `
                    <div class="country-card" onclick="quickSearchCountry('${c.name}')">
                        <div class="country-flag">${getCountryEmoji(c.code)}</div>
                        <div class="country-info">
                            <h4>${c.name}</h4>
                            <p>${c.job_count} open jobs</p>
                        </div>
                    </div>
                `).join("");
            }
        }
        
    } catch (err) {
        console.error("Failed to bootstrap home feeds:", err);
        if (latestGrid) {
            latestGrid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; border-color: rgba(244, 63, 94, 0.2);">
                    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                    <h3>Backend Connection Offline</h3>
                    <p>The Global Search backend service is offline. Please launch the FastAPI server (main.py) to activate real-time search.</p>
                </div>
            `;
        }
    }
}

// Convert Country ISO Codes to beautiful flags emojis
function getCountryEmoji(countryCode) {
    if (!countryCode || countryCode === "GL") return "🌐";
    const codePoints = countryCode
        .toUpperCase()
        .split('')
        .map(char =>  127397 + char.charCodeAt(0));
    return String.fromCodePoint(...codePoints);
}

// Quick Navigation Search helpers
function quickSearchTag(tag) {
    const isPages = window.location.pathname.includes("pages/");
    window.location.href = isPages 
        ? `search.html?keyword=${encodeURIComponent(tag)}` 
        : `frontend/pages/search.html?keyword=${encodeURIComponent(tag)}`;
}

function quickSearchCountry(countryName) {
    const isPages = window.location.pathname.includes("pages/");
    window.location.href = isPages 
        ? `search.html?country=${encodeURIComponent(countryName)}` 
        : `frontend/pages/search.html?country=${encodeURIComponent(countryName)}`;
}

function executePrimarySearch() {
    const keywordInput = document.getElementById("primary-search-keyword");
    const locationInput = document.getElementById("primary-search-location");
    
    const kw = keywordInput ? keywordInput.value.trim() : "";
    const loc = locationInput ? locationInput.value.trim() : "";
    
    const isPages = window.location.pathname.includes("pages/");
    const searchUrl = isPages ? "search.html" : "frontend/pages/search.html";
    
    window.location.href = `${searchUrl}?keyword=${encodeURIComponent(kw)}&country=${encodeURIComponent(loc)}`;
}

function imgFallback(img, initials) {
    img.outerHTML = `<div class="company-logo company-logo-init">${initials}</div>`;
}

function isFakeSearchLink(link) {
    if (!link || !link.startsWith('http')) return true;
    const patterns = [/ref=\d+/i, /refId=\d+/i, /\/search\//i, /[?&]q=/i, /[?&]keywords=/i, /[?&]term=/i];
    return patterns.some(p => p.test(link));
}

function getApplyUrl(job) {
    const link = job.apply_link;
    if (!link || !link.startsWith('http') || isFakeSearchLink(link)) {
        const base = window.location.pathname.includes("pages/") ? '' : 'frontend/pages/';
        return `${base}details.html?id=${job.id}`;
    }
    if (link.includes('karmakarta.com')) {
        const base = window.location.pathname.includes("pages/") ? '' : 'frontend/pages/';
        return `${base}details.html?id=${job.id}`;
    }
    if (link.includes('psc.gov.np') && (link.includes('/?s=') || link.includes('/notice/'))) {
        const base = window.location.pathname.includes("pages/") ? '' : 'frontend/pages/';
        return `${base}details.html?id=${job.id}`;
    }
    return link;
}
