# Job Tracker ATS

A local-first job application tracker for QA / SDET / test-engineering job searches. Log every role you apply to, move it through a drag-and-drop kanban board, and get live ATS keyword-coverage insights against an editable library of in-demand testing keywords.

**Live demo:** [https://job-tracker-ats.vercel.app](https://job-tracker-ats.vercel.app)

## Features

- **Kanban board** — Wishlist → Applied → Follow-up columns with drag-and-drop reordering (`@dnd-kit`).
- **ATS analyzer** — Pastes a job description (or marks covered keywords) and computes a match score against a curated keyword library for modern QA/SDET roles. Shows what's matched and what's missing, grouped into categories such as Test Automation, API, CI/CD, Mobile, Performance, Data & SQL, and more.
- **Editable keyword library** — Keyword groups are editable at runtime and persisted in the browser.
- **Resume tracking** — Attach a resume label to each job; track salaries, notes, and application dates.
- **100% local & private** — All data is stored in IndexedDB (`idb`) in your browser. Nothing leaves your machine; no backend or account required.
- **Search & theme** — Instant company/role search and a dark/light theme with system detection.

## Tech Stack

- [React 19](https://react.dev) + [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vite.dev) build tooling
- [@dnd-kit](https://dndkit.com) for drag-and-drop
- [idb](https://github.com/jakearchibald/idb) for IndexedDB persistence
- [date-fns](https://date-fns.org) for date handling
- [lucide-react](https://lucide.dev) for icons

## Getting Started

```bash
# Install dependencies
npm install

# Start the dev server
npm run dev

# Lint
npm run lint

# Type-check and production build
npm run build

# Preview the production build locally
npm run preview
```

## Project Structure

```
src/
├── App.tsx              # Root component, state + handlers
├── types.ts             # Job / drag & drop / ATS domain types
├── lib/
│   ├── db.ts            # IndexedDB schema and helpers
│   ├── keywordLib.ts    # Default ATS keyword groups + scoring logic
│   ├── uid.ts           # ID generation
│   └── useJobs.ts       # React hook wrapping the data layer
└── components/
    ├── Board.tsx        # Kanban board
    ├── Column.tsx       # Single board column
    ├── JobCard.tsx      # Job card in a column
    ├── JobModal.tsx     # Create / edit job dialog
    ├── Hero.tsx         # Header with counts + ATS score
    ├── Sidebar.tsx      # Collapsible sidebar
    ├── TopBar.tsx       # Search, theme toggle, add button
    └── Toasts.tsx       # Toast notifications
```

## Deployment

The app is configured for [Vercel](https://vercel.com) and linked to the `job-tracker-ats` project. Production deploys are proxied through `job-tracker-ats.vercel.app`.

```bash
# One-step build + deploy to production
./deploy.bat

# Or manually
vercel login
vercel --prod --yes
```

## Data & Privacy

Because all data lives in your browser's IndexedDB, clearing browser storage resets the app. There is no cloud sync. Clear cache/local storage for this site to delete all tracked data.