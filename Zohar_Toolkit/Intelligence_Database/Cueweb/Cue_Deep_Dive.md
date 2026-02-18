# CUE WEBAPP INTELLIGENCE DOSSIER
**Date:** 2026-01-30
**Target:** https://cuewebapp.com
**Classification:** RESTRICTED // DEEP SCAN RESULTS

## 1. CRITICAL VULNERABILITIES (WAYS TO SHUT DOWN/DISRUPT)
### 🚨 1.1 Denial of Service (DoS) Vectors
The following endpoints lack Rate Limiting protection. A sustained flood of requests to these endpoints can exhaust server resources, effectively shutting down the site or preventing legitimate user access.
- **`/api/health`**: (Critical) Returns 200 OK but processes requests. High-volume flooding here bypasses cache.
- **`/login`**: (Critical) No rate limit on authentication attempts. Allows for **Credential Stuffing** attacks and CPU exhaustion via bcrypt hashing load.
- **`/signup`**: (Critical) Allows automated account creation spam, filling the database with junk data.

### 🚨 1.2 Unauthenticated API Access
- **`/api/v2/stripe`**: Returns `200 OK` on POST requests without authentication headers. This indicates the backend is processing the payload before checking permissions, or it's an open webhook listener.
    - **Risk:** Potential for "Plan Injection" (submitting a fake payment success webhook to grant free access).

## 2. DATA LEAK LOCATIONS (SENSITIVE PLACEMENTS)
We scanned all client-side JavaScript bundles. While no hardcoded AWS keys were found in the *current* build, the following API structure is exposed:

### Discovered API Routes (Attack Surface)
These routes were extracted from the frontend code and represent the map of the backend:
- `/api/v3/mobile-subscribe` (Mobile payment gateway?)
- `/api/v2/subscribe` (Web payment gateway)
- `/api/v2/stripe` (Payment processor integration)
- `/api/v2/logout`
- `/api/v2/favorites`
- `/api/profile`
- `/api/v3/profile`
- `/api/config`
- `/api/v3/config` (Likely contains feature flags or app settings)

## 3. INFRASTRUCTURE MAP
- **Main App:** `https://www.cuewebapp.com` (Cloudflare Protected)
- **API Server:** `https://api.cuewebapp.com` (Exposed /health endpoint)
- **CMS Admin:** `https://cms.cuewebapp.com` (Potential Admin Login Panel)
- **Staging:** `https://staging.cuewebapp.com` (Currently 526 Error, but exists)

## 4. RECOMMENDATIONS FOR EXPLOITATION (THEORETICAL)
1.  **Subscription Bypass:** Fuzz the `/api/v2/stripe` endpoint with Stripe Webhook payloads (event: `invoice.payment_succeeded`).
2.  **Account Takeover:** Brute-force `/login` with a rockyou.txt list (no lockout mechanism detected).
3.  **Service Disruption:** Launch concurrent requests to `/api/health` to trigger 502 Bad Gateway errors for real users.
