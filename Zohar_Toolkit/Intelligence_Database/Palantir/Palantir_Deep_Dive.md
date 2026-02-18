# PALANTIR DEEP DIVE: ARCHITECTURE & TARGET
**Date:** 2026-01-30

## 1. SOFTWARE MECHANICS (AIP & FOUNDRY)

### DISCOVERED SUBDOMAINS (Active Brute-Force)
- https://www.palantir.com [200] -> https://www.palantir.com/
- https://api.palantir.com [200] -> https://www.palantir.com/docs/foundry/api
- https://docs.palantir.com [200] -> https://www.palantir.com/docs
- https://learn.palantir.com [200] -> https://learn.palantir.com/
- https://blog.palantir.com [403] -> https://blog.palantir.com/
- https://investors.palantir.com [200] -> https://investors.palantir.com/
### Source: https://www.palantir.com/docs/foundry/aip/aip-features/
**Technical Stack Detected:**
- Internal Components: Foundry, Gotham, Apollo

**Operational Mechanics (Snippets):**
> ...Search Palantir Documentation Documentation Apollo Gotham Search documentation Search karat + K API Reference â Send feedback en en jp kr zh AB XY AB XY AB XY AB XY AB XY AB XY AB XY Capabilities AI Platform (AIP) Data connectivity & integration Model connectivity & development Ontology building Developer toolchain Use case development Analytics Product delivery Security & governance Management & enablement Getting started Architecture center Platform updates Announcements Release notes AI Platform (AIP) Hide sidebar Overview AIP features Get started with AIP Best practices for LLM prompt engineering Supported LLMs AI ethics and governance AIP security and privacy Compute usage with AIP Administration Enable AIP features LLM capacity management Bring your own model Bring your own model to AIP Register an LLM using function interfaces Use registered LLM Release notes â Applications AIP Agent Studio Overview Core concepts Getting started Application state Retrieval context Context types Citations Tools Overview Use commands as tools in AIP Agent Studio Agents as Functions Distribute AIP Agents using Marketplace Use AIP Agents through Foundry APIs AIP Analyst Overview Core concepts Analysis configuration Workshop widget AIP Assist Overview AIP Assist best practices Power AIP Assist with custom content sources Overview Register custom content sources Serve custom content sources to users Deploy custom source-backed AIP Agents Custom content source best practices AIP Assist application integrations Suggested actions in AIP Assist AI FDE Overview Navigation Best practices AIP Evals Overview Evaluation suites for Logic functions Create an evaluation suite Use intermediate parameters to evaluate block output Evaluate Ontology edits Run an evaluation suite Run experiments Write run results to a dataset Analyze run results View results in metrics dashboard AIP Logic Overview Core concepts Getting started Blocks Automate AIP Logic Compute usage Execution mode settings Branching AIP Logic FAQ AIP Model Catalog Overview Model deprecation AIP Observability Overview Execution history Tracing Logging and debugging Log permissions Performance monitoring and optimization AIP Threads Overview Getting started AIP Document Intelligence Overview Core concepts AI Platform (AIP) AIP features AIP features Applications across the Palantir platform are equipped with AIP-powered capabilities, as described on this page....
> ...AIP applications and builder capabilities AIP enables developers and builders to create LLM-backed workflows, agents, and applications in the Palantir platform using LLM-native tools like AIP Agent Studio and AIP Logic , or AIP-accelerated platform applications like Pipeline Builder and Workshop ....
> ...Pipeline Builder Use AIP in Pipeline Builder to help you better understand, build, and manage your pipeline....

---
### Source: https://www.palantir.com/docs/foundry/aip/aip-security/
**Technical Stack Detected:**
- Protocols: rest
- Internal Components: Foundry, Gotham, Apollo

**Operational Mechanics (Snippets):**
> ...Search Palantir Documentation Documentation Apollo Gotham Search documentation Search karat + K API Reference â Send feedback en en jp kr zh AB XY AB XY AB XY AB XY AB XY AB XY AB XY Capabilities AI Platform (AIP) Data connectivity & integration Model connectivity & development Ontology building Developer toolchain Use case development Analytics Product delivery Security & governance Management & enablement Getting started Architecture center Platform updates Announcements Release notes AI Platform (AIP) Hide sidebar Overview AIP features Get started with AIP Best practices for LLM prompt engineering Supported LLMs AI ethics and governance AIP security and privacy Compute usage with AIP Administration Enable AIP features LLM capacity management Bring your own model Bring your own model to AIP Register an LLM using function interfaces Use registered LLM Release notes â Applications AIP Agent Studio Overview Core concepts Getting started Application state Retrieval context Context types Citations Tools Overview Use commands as tools in AIP Agent Studio Agents as Functions Distribute AIP Agents using Marketplace Use AIP Agents through Foundry APIs AIP Analyst Overview Core concepts Analysis configuration Workshop widget AIP Assist Overview AIP Assist best practices Power AIP Assist with custom content sources Overview Register custom content sources Serve custom content sources to users Deploy custom source-backed AIP Agents Custom content source best practices AIP Assist application integrations Suggested actions in AIP Assist AI FDE Overview Navigation Best practices AIP Evals Overview Evaluation suites for Logic functions Create an evaluation suite Use intermediate parameters to evaluate block output Evaluate Ontology edits Run an evaluation suite Run experiments Write run results to a dataset Analyze run results View results in metrics dashboard AIP Logic Overview Core concepts Getting started Blocks Automate AIP Logic Compute usage Execution mode settings Branching AIP Logic FAQ AIP Model Catalog Overview Model deprecation AIP Observability Overview Execution history Tracing Logging and debugging Log permissions Performance monitoring and optimization AIP Threads Overview Getting started AIP Document Intelligence Overview Core concepts AI Platform (AIP) AIP security and privacy AIP security and privacy Palantir is committed to protecting the privacy and security of customer data....

---
### Source: https://www.palantir.com/docs/foundry/aip/bring-your-own-model/
**Technical Stack Detected:**
- Protocols: REST
- Data Formats: Json, json
- Internal Components: foundry, Foundry, Gotham, Apollo

**Operational Mechanics (Snippets):**
> ...Search Palantir Documentation Documentation Apollo Gotham Search documentation Search karat + K API Reference â Send feedback en en jp kr zh AB XY AB XY AB XY AB XY AB XY AB XY AB XY Capabilities AI Platform (AIP) Data connectivity & integration Model connectivity & development Ontology building Developer toolchain Use case development Analytics Product delivery Security & governance Management & enablement Getting started Architecture center Platform updates Announcements Release notes AI Platform (AIP) Hide sidebar Overview AIP features Get started with AIP Best practices for LLM prompt engineering Supported LLMs AI ethics and governance AIP security and privacy Compute usage with AIP Administration Enable AIP features LLM capacity management Bring your own model Bring your own model to AIP Register an LLM using function interfaces Use registered LLM Release notes â Applications AIP Agent Studio Overview Core concepts Getting started Application state Retrieval context Context types Citations Tools Overview Use commands as tools in AIP Agent Studio Agents as Functions Distribute AIP Agents using Marketplace Use AIP Agents through Foundry APIs AIP Analyst Overview Core concepts Analysis configuration Workshop widget AIP Assist Overview AIP Assist best practices Power AIP Assist with custom content sources Overview Register custom content sources Serve custom content sources to users Deploy custom source-backed AIP Agents Custom content source best practices AIP Assist application integrations Suggested actions in AIP Assist AI FDE Overview Navigation Best practices AIP Evals Overview Evaluation suites for Logic functions Create an evaluation suite Use intermediate parameters to evaluate block output Evaluate Ontology edits Run an evaluation suite Run experiments Write run results to a dataset Analyze run results View results in metrics dashboard AIP Logic Overview Core concepts Getting started Blocks Automate AIP Logic Compute usage Execution mode settings Branching AIP Logic FAQ AIP Model Catalog Overview Model deprecation AIP Observability Overview Execution history Tracing Logging and debugging Log permissions Performance monitoring and optimization AIP Threads Overview Getting started AIP Document Intelligence Overview Core concepts AI Platform (AIP) Bring your own model Bring your own model to AIP Bring your own model to AIP Bring-your-own-model (BYOM), also known as "registered models" in the Palantir platform, is a capability that provides first-class support for customers who want to connect their own LLMs or accounts to use in AIP with all Palantir developer products....
> ...These products include AIP Logic, Pipeline Builder, Agent Studio, Workshop, and more....
> ...Application Supported Caveats Functional interfaces supported AIP Logic Yes ChatCompletion, ChatCompletionWithVision Pipeline Builder Yes Provider must have REST endpoint, as function must be implemented with no webhooks....

---
### Source: https://www.palantir.com/docs/foundry/data-integration/architecture/
**Technical Stack Detected:**

**Operational Mechanics (Snippets):**

---

## 2. TARGET: MELISSA M (melissam@palantir.com)
**Profile Analysis:**
- **Email Pattern:** Firstname + Last Initial (Standard Corporate).
- **Role Hypothesis:** Likely PR/Comms/HR given the public exposure of the email.
- **Username Reuse:** 'melissam' is a very common handle. Direct username matches are likely False Positives unless corroborated by Palantir context.

**Recommended Search Vectors (Dorks):**
Run these to find direct footprints:
1. `site:linkedin.com "Palantir" "Melissa"`
2. `"melissam@palantir.com"`
