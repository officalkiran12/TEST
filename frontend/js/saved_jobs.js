/**
 * ==========================================================================
 * SAVED JOBS MANAGER (HYBRID LOCAL STORAGE + CLOUD SYNC ENGINE)
 * ==========================================================================
 */
const API_BASE = "http://127.0.0.1:8000/api";

const SavedJobsManager = {
    // Retrieve locally saved job IDs
    getLocalIds() {
        try {
            const ids = localStorage.getItem("saved_job_ids");
            return ids ? JSON.parse(ids) : [];
        } catch (e) {
            console.error("Failed to read localStorage:", e);
            return [];
        }
    },

    // Retrieve full locally saved jobs
    getLocalJobs() {
        try {
            const jobs = localStorage.getItem("saved_jobs_data");
            return jobs ? JSON.parse(jobs) : [];
        } catch (e) {
            console.error("Failed to read localStorage:", e);
            return [];
        }
    },

    isSaved(jobId) {
        return this.getLocalIds().includes(Number(jobId));
    },

    async toggleSave(job, cardBtnElement = null) {
        const jobId = Number(job.id);
        let ids = this.getLocalIds();
        let jobs = this.getLocalJobs();
        const saved = this.isSaved(jobId);

        if (saved) {
            // 1. Remove Locally
            ids = ids.filter(id => id !== jobId);
            jobs = jobs.filter(j => Number(j.id) !== jobId);
            localStorage.setItem("saved_job_ids", JSON.stringify(ids));
            localStorage.setItem("saved_jobs_data", JSON.stringify(jobs));

            // Update UI element if provided
            if (cardBtnElement) {
                cardBtnElement.classList.remove("saved");
                cardBtnElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>`;
            }

            // Show Toast Alert
            showNotification(`Job removed from saved bookmarks.`, "rose");

            // 2. Remove Cloud Synced
            try {
                await fetch(`${API_BASE}/saved/${jobId}`, { method: "DELETE" });
            } catch (err) {
                console.warn("Could not sync unsave to cloud. Saved locally.");
            }
        } else {
            // 1. Save Locally
            ids.push(jobId);
            jobs.push(job);
            localStorage.setItem("saved_job_ids", JSON.stringify(ids));
            localStorage.setItem("saved_jobs_data", JSON.stringify(jobs));

            // Update UI element if provided
            if (cardBtnElement) {
                cardBtnElement.classList.add("saved");
                cardBtnElement.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #f43f5e;"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>`;
            }

            // Show Toast Alert
            showNotification(`Job saved to bookmarks!`, "emerald");

            // 2. Save Cloud Synced
            try {
                await fetch(`${API_BASE}/saved?job_id=${jobId}`, { method: "POST" });
            } catch (err) {
                console.warn("Could not sync save to cloud. Saved locally.");
            }
        }
    },

    // Sync local Storage with backend DB (called on saved jobs page load)
    async syncWithServer() {
        try {
            const res = await fetch(`${API_BASE}/saved`);
            if (res.status === 200) {
                const serverJobs = await res.json();
                const serverIds = serverJobs.map(j => Number(j.id));
                
                // Update local storage with fresh server data
                localStorage.setItem("saved_job_ids", JSON.stringify(serverIds));
                localStorage.setItem("saved_jobs_data", JSON.stringify(serverJobs));
                return serverJobs;
            }
        } catch (err) {
            console.warn("Could not sync with server. Using local cache instead.");
        }
        return this.getLocalJobs();
    }
};

// Helper to show modern floating notifications
function showNotification(message, colorClass = "cyan") {
    // Check if element exists, create if not
    let banner = document.getElementById("system-notification-banner");
    if (!banner) {
        banner = document.createElement("div");
        banner.id = "system-notification-banner";
        banner.className = "alert-banner";
        document.body.appendChild(banner);
    }

    // Set accent border color class
    let borderColor = "#06b6d4";
    if (colorClass === "rose") borderColor = "#f43f5e";
    if (colorClass === "emerald") borderColor = "#10b981";
    if (colorClass === "violet") borderColor = "#8b5cf6";

    banner.style.borderColor = borderColor;
    banner.innerHTML = `
        <span style="font-weight: 500;">${message}</span>
        <button class="alert-banner-close" onclick="this.parentElement.classList.remove('show')">&times;</button>
    `;
    
    banner.classList.add("show");
    
    // Auto hide after 4 seconds
    setTimeout(() => {
        banner.classList.remove("show");
    }, 4000);
}
