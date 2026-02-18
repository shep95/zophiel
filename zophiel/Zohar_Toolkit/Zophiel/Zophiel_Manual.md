# ZOPHIEL: The Spy of God
## Intelligence Analyst Manual

**Version:** 1.0.0  
**Clearance:** ZOHAR_ROOT  

---

### 1. Philosophy
Zophiel is not a "scraper." It is an automated intelligence analyst. It mimics the behavior of a human researcher performing deep-dive OSINT (Open Source Intelligence) investigations using DuckDuckGo.

Unlike brute-force tools that use "Google Dorks" (which often trigger CAPTCHAs and bot detection), Zophiel uses **Natural Language Triangulation**. It asks the search engine questions in a way that surfaces organic results.

### 2. The Protocol
When you run Zophiel, it executes a multi-phase investigation:

#### Phase I: Triangulation
*   **Objective:** Confirm identity by cross-referencing Name + Location + Employer.
*   **Query Style:** `"John Doe" "New York" "Goldman Sachs"`
*   **Why:** This establishes the "Ground Truth" profile.

#### Phase II: Professional Mapping
*   **Objective:** Locate the primary digital resume (LinkedIn, Xing, Corporate bios).
*   **Query Style:** `John Doe linkedin` (Natural) instead of `site:linkedin.com` (Dork).

#### Phase III: Document Hunting
*   **Objective:** Find leaked or public files (PDFs, DOCX, PPT).
*   **Query Style:** `"John Doe" filetype:pdf`
*   **Intel Value:** Resumes, conference slides, court documents, and newsletters often contain direct contact info (emails/phone numbers) that web pages hide.

#### Phase IV: Contact Discovery
*   **Objective:** Uncover direct communication channels.
*   **Query Style:** `"John Doe" email contact` or `"John Doe" @gmail.com`

### 3. Usage
Run the core engine directly from the terminal:

```bash
python zophiel_core.py
```

Follow the prompts. 

*   **Target Name:** Full legal name is best.
*   **Location:** City/State helps reduce false positives.
*   **Employer:** Current or past company locks in the identity.

---
*"And Zophiel was the spy of God, seeing all that was hidden in the garden."*
