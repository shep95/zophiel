# Zohar Intelligence API: Integration Guide for AI Agents

**Subject:** Integrating Zohar Toolkit (OSINT Engine) via REST API for Chat Interfaces
**Target Audience:** AI Builders / Frontend Developers
**Version:** 2.0 (FastAPI + Zophiel Engine)

---

## 1. System Overview
The Zohar Toolkit exposes a **FastAPI** backend that acts as the intelligence engine. Your AI Chatbot (the "Frontend") will function as the *Interrogator*, sending structured requests to the API and receiving raw intelligence reports, which it then summarizes for the user.

**Workflow:**
1. **User:** "Find out everything about John Doe in Miami."
2. **AI Chatbot:** Parses intent -> Extracts `target_name="John Doe"`, `location="Miami"`.
3. **AI Chatbot:** Sends `POST /api/v1/investigate` to Zohar API.
4. **Zohar API:** Runs `ZophielEngine` (DuckDuckGo Scraper + PII Extractor).
5. **Zohar API:** Returns JSON Dossier (Phones, Emails, Criminal Records, Socials).
6. **AI Chatbot:** Reads JSON -> Generates natural language response.

---

## 2. API Connection Details

### Base URL
*   **Production:** `https://your-railway-app-url.up.railway.app` (Replace with actual URL)
*   **Local:** `http://localhost:8000`

### Authentication
*   *Currently Open (Public).* 
*   *Future:* Add `Authorization: Bearer <API_KEY>` header if you lock it down.

---

## 3. Endpoints for AI Usage

### A. The Primary Weapon: `run_investigation`
This is the main endpoint the AI should call when a user asks for intel.

*   **Endpoint:** `POST /api/v1/investigate`
*   **Content-Type:** `application/json`

**Request Body Schema:**
```json
{
  "target_name": "string",       // REQUIRED: Full Name (e.g., "Gary Grinberg")
  "location": "string",          // OPTIONAL: City/State (e.g., "Miami, FL")
  "employer": "string"           // OPTIONAL: Company Name (e.g., "GG33")
}
```

**Example Curl:**
```bash
curl -X POST "https://your-app-url.com/api/v1/investigate" \
     -H "Content-Type: application/json" \
     -d '{"target_name": "Gary Grinberg", "location": "Miami"}'
```

**Response (JSON Dossier):**
```json
{
  "status": "success",
  "target": "Gary Grinberg",
  "confidence_score": 85,
  "confirmed_intelligence": [
    {
      "sector": "legal_criminal",
      "title": "Gary Grinberg vs. Nationwide Insurance (RICO Case)",
      "url": "https://insurancejournal.com/news/...",
      "snippet": "Principal defendant in $100M insurance fraud case...",
      "scraped_content": "Full text of the article..."
    }
  ],
  "unverified_leads": [
    {
      "sector": "social_media",
      "url": "https://twitter.com/gg33",
      "title": "GG33 Academy"
    }
  ],
  "pii_extracted": {
    "phones": ["305-555-0199"],
    "emails": ["gary@gg33.com"]
  }
}
```

---

## 4. Instructions for the AI Builder (Prompt Engineering)

Give your AI (the "Builder" or "Agent") these specific instructions:

> **"You are integrating a Python-based OSINT engine called 'Zohar'. It is hosted on Railway. When the user asks to investigate a person, do NOT try to search the web yourself. Instead, formulate a JSON payload with `target_name` and `location` and send a POST request to the Zohar API endpoint `/api/v1/investigate`. Wait for the JSON response. When you receive the JSON, do not just dump it. Roleplay as an Intelligence Analyst. Read the 'confirmed_intelligence' section and summarize the findings into a briefing. Highlight any 'pii_extracted' (phones/emails) as 'High Value Targets'."**

---

## 5. Handling Latency
**Warning:** Real-time OSINT takes time (15-45 seconds) because the server is actively scraping DuckDuckGo and visiting websites.
*   **UI Tip:** Tell the AI Builder to show a "Scanning..." or "Deploying Agents..." animation while waiting for the `POST` request to complete.
