# Zophiel Integration & Architecture

## Overview
Zophiel is a powerful Python-based OSINT engine. To integrate it into a web application (like `cuewebapp.com`), you need a client-server architecture. The browser (Frontend) cannot run Python scripts directly; it must talk to a Backend API.

## Architecture Diagram

```
[User Browser]  <--HTTP JSON-->  [Backend API (FastAPI)]  <--Python-->  [Zophiel Engine]
     |                                   |                                     |
     |                                   |                                     |
[Frontend UI]                        [OpenAI API] <--(Optional)           [DuckDuckGo]
(React/Vue/JS)                       (For Summaries)                       (The Web)
```

## Workflow Steps

1.  **Frontend (The Website):**
    *   User enters "Asher Shepherd Newton" and "Cape Coral" into a form.
    *   Frontend sends a `POST` request to your backend:
        ```json
        POST /api/v1/investigate
        {
          "target_name": "Asher Shepherd Newton",
          "location": "Cape Coral"
        }
        ```

2.  **Backend (The API Server):**
    *   Receives the request.
    *   Calls `ZophielEngine.ignite()`.
    *   (Optional) Sends the raw JSON report to **OpenAI (GPT-4)** with a prompt: *"Act as an intelligence analyst. Summarize this JSON report into a dossier."*
    *   Returns the final JSON (with the summary) to the frontend.

3.  **Frontend (Display):**
    *   Receives the JSON.
    *   Renders the "Confirmed Intelligence" cards and the "Analyst Summary" text.

## Do you need OpenAI?
**No**, not for the scraping itself. Zophiel does the work.
**Yes**, if you want the tool to "talk" like an analyst.
*   **Without OpenAI:** The user gets a list of links and data points (Raw Intelligence).
*   **With OpenAI:** The user gets a written report explaining *what the data means* (Finished Intelligence).

## Setup Guide

1.  **Start the API Server:**
    ```bash
    cd Zohar_Toolkit/Zophiel
    uvicorn zophiel_api:app --reload
    ```

2.  **Test the Endpoint:**
    You can visit `http://127.0.0.1:8000/docs` to see the interactive API documentation.
