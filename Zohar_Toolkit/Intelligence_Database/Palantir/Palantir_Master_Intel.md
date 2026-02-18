# MASTER INTELLIGENCE DOSSIER: PALANTIR TECHNOLOGIES (PLTR)
**Classification:** OPEN SOURCE INTELLIGENCE (OSINT)  
**Target:** Palantir Technologies Inc.  
**Primary Domain:** `palantir.com`  
**Generated:** 2026-01-30  

---

## 1. EXECUTIVE SUMMARY
Palantir Technologies operates a highly compartmentalized digital infrastructure. Their public-facing presence (`palantir.com`) is a "static shell" hosted on Amazon S3 and cached via Fastly, designed to be permissive to bots but containing no operational logic. The actual core platforms (Foundry, Gotham, Apollo) are air-gapped or hosted on hidden/customer-specific subdomains.

**Critical Findings:**
*   **Infrastructure:** AWS S3 (Frontend) + Fastly (CDN/WAF).
*   **Bot Defense:** Surprisingly weak on public domains (No Captcha, No UA blocking).
*   **Key Personnel:** Identified `melissam@palantir.com` (Likely PR/Comms) and `employee-verifications@palantir.com` (HR).
*   **Software Mechanics:** Confirmed usage of "Ontology" mapping, REST APIs for model integration, and "Apollo" for continuous delivery in disconnected environments.

---

## 2. INFRASTRUCTURE & TECH STACK
### Hosting & Network
*   **Frontend Server:** `AmazonS3` (Static Bucket Hosting).
*   **Content Delivery (CDN):** `Fastly` (Cache ID: `cache-mrs...`).
*   **WAF Status:** **Permissive**. Fastly is configured for caching, not aggressive blocking.
    *   *Vulnerability:* Standard Python scripts and empty User-Agents are **ALLOWED** (HTTP 200).
    *   *Implication:* Public data scraping is trivial and requires no evasion techniques.

### Third-Party Integrations (Data Flow)
*   **Recruiting Data:** Flows to **Lever** (`api.lever.co`).
*   **Marketing Tracking:** Flows to **Marketo** (`mktoutil.com`).
*   **Analytics:** Flows to **Heap Analytics** (`heapanalytics.com`).
*   **Compliance/Cookies:** Managed by **OneTrust**.

### Subdomain Reconnaissance
*   `www.palantir.com` (Main Marketing)
*   `investors.palantir.com` (Financials)
*   `resources.palantir.com` (Assets)
*   `palantir.io` (Secondary Domain)

---

## 3. SOFTWARE ARCHITECTURE (FOUNDRY & AIP)
*Intelligence derived from internal documentation scraping (`/docs/foundry/aip/...`)*

### The "Ontology" (Core Concept)
Palantir's software relies on a semantic layer called the **Ontology**. It does not just store rows/columns; it maps data to "Real World Objects" (e.g., *Aircraft*, *Factory*, *Soldier*).
*   **AIP Agents:** AI agents use the Ontology to perform actions.
*   **Function Interfaces:** External LLMs can be registered as "Functions" via **REST API**.

### Critical Components
1.  **Apollo:** The continuous delivery platform. It updates software in "disconnected" environments (e.g., submarines, classified networks). *High-Value Target for infrastructure intel.*
2.  **Gotham:** The defense/intelligence product (Graph-based).
3.  **Foundry:** The commercial data integration product.
4.  **Pipeline Builder:** The ETL tool that ingests data (Supports Parquet, Avro, Delta Lake).

### Protocols & Standards
*   **API Access:** REST, gRPC.
*   **Data Formats:** JSON, Parquet.
*   **Auth Methods:** OAuth, SAML, OIDC (Standard Enterprise Stack).

---

## 4. HUMAN INTELLIGENCE (HUMINT)
### Target: Melissa M.
*   **Selector:** `melissam@palantir.com`
*   **Role Assessment:** **Global Communications / PR**.
    *   *Evidence:* Email is exposed on public facing pages, typical for press contacts.
    *   *Naming Convention:* `[Firstname][LastInitial]@palantir.com` (Standard Corporate).
*   **Digital Footprint:**
    *   Twitter: `@melissam` (Likely match, high probability).
    *   GitHub: `@melissam` (Common handle, low confidence linkage without repo correlation).
*   **Risk Level:** **Low**. This is a public channel likely monitored by a team, not a direct line to a developer or admin.

### Other Key Contacts
*   `employee-verifications@palantir.com` (HR/Legal Channel)
*   `media@palantir.com` (General Press)
*   `investors@palantir.com` (IR Channel)

---

## 5. OPERATIONAL SECURITY (OPSEC) OBSERVATIONS
1.  **The "Air Gap" Strategy:** Palantir separates their marketing site (low security) from their product portals (high security). You cannot pivot from `palantir.com` to `foundry` access easily.
2.  **Obfuscation:** Employee names are scrubbed from the site. Only generic aliases (`media@`, `investors@`) or specific PR contacts (`melissam@`) are visible.
3.  **Bot Trap Absence:** The lack of Captchas on the main site suggests they *want* their marketing material to be scraped/indexed by search engines, reserving defenses for the actual login pages.

---
**END OF DOSSIER**
