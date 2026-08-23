export type JobStatus = 'wishlist' | 'applied' | 'followup'

export interface Job {
  id: string
  company: string
  role: string
  url: string
  resume: string
  dateApplied: string // ISO date (yyyy-MM-dd)
  salary: string
  notes: string
  status: JobStatus
  /** Keywords the candidate covers for this role. */
  keywords: string[]
  /** Required keywords (from the job / analyzer) not yet covered. */
  missingKeywords: string[]
  /** Optional pasted job description used by the ATS analyzer. */
  jdText: string
  createdAt: number
}

export type JobDraft = Omit<Job, 'id' | 'createdAt'>

export interface ColumnMeta {
  id: JobStatus
  title: string
  subtitle: string
}

export const COLUMNS: ColumnMeta[] = [
  { id: 'wishlist', title: 'Wishlist', subtitle: 'Saved, not applied yet' },
  { id: 'applied', title: 'Applied', subtitle: 'Application submitted' },
  { id: 'followup', title: 'Follow-up', subtitle: 'Recruiter / referral pinged' },
]

export const STATUS_LABEL: Record<JobStatus, string> = {
  wishlist: 'Wishlist',
  applied: 'Applied',
  followup: 'Follow-up',
}

export interface KeywordGroup {
  id: string
  label: string
  keywords: string[]
}

export interface AtsResult {
  score: number
  matched: string[]
  missing: string[]
  foundCount: number
  totalCount: number
}

/** Ensure a date string is a valid yyyy-MM-dd, else today. */
export function normalizeDate(value: string): string {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value) && !Number.isNaN(new Date(value).getTime())) {
    return value
  }
  return new Date().toISOString().slice(0, 10)
}

export function toDraft(job: Job): JobDraft {
  const { id: _id, createdAt: _createdAt, ...draft } = job
  return draft
}