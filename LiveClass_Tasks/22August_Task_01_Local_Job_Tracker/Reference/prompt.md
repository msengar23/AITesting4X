## Prompt to Create your own Job Tracker AI (localhost)

Create a local-first Job Tracker as a single-page React application scaffolded with Vite. All data must persist in the browser using IndexedDB (use the `idb` library for a cleaner async API). No backend or authentication is needed.

Data Model — Each job card stores:

- Company name (text, required)

- Job title / role (text, required)

- LinkedIn job URL (URL, clickable)

- Resume used (text / dropdown of previously used resume names, e.g., "SDE_Resume_v3", "QA_Lead_Resume")

- Date applied (auto-set on creation, editable)

- Salary range (optional text, e.g., "₹25-30 LPA" or "$150-180K")

- Notes (optional textarea for recruiter name, referral info, etc.)

- Status (maps to Kanban column)

Kanban Columns (drag-and-drop between them):

1. Wishlist — Saved jobs I haven't applied to yet

2. Applied — Application submitted

3. Follow-up — Followed up with recruiter / referral