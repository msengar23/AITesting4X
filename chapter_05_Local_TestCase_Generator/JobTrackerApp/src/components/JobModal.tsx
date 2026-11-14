import { useMemo, useState } from 'react'
import { Scan, X } from 'lucide-react'
import type { Job, JobDraft, JobStatus, KeywordGroup } from '../types'
import { COLUMNS, normalizeDate, toDraft } from '../types'
import { flattenKeywords } from '../lib/keywordLib'

interface Props {
  open: boolean
  initial: Job | null // null = create, Job = edit
  status?: JobStatus // pre-filled column when creating
  resumes: string[]
  groups: KeywordGroup[]
  onClose: () => void
  onSubmit: (draft: JobDraft, id?: string) => void
}

const EMPTY: JobDraft = {
  company: '',
  role: '',
  url: '',
  resume: '',
  dateApplied: new Date().toISOString().slice(0, 10),
  salary: '',
  notes: '',
  keywords: [],
  missingKeywords: [],
  jdText: '',
  status: 'wishlist',
}

function buildInitial(initial: Job | null, status: JobStatus | undefined): JobDraft {
  if (initial) return toDraft(initial)
  return {
    ...EMPTY,
    dateApplied: new Date().toISOString().slice(0, 10),
    status: status ?? 'wishlist',
  }
}

export function JobModal({ open, initial, status, resumes, groups, onClose, onSubmit }: Props) {
  const [form, setForm] = useState<JobDraft>(() => buildInitial(initial, status))
  const [resumeMode, setResumeMode] = useState<'existing' | 'new'>(() =>
    initial?.resume && resumes.includes(initial.resume) ? 'existing' : 'new',
  )
  const [errors, setErrors] = useState<{ company?: string; role?: string }>({})

  const allKeywords = useMemo(() => flattenKeywords(groups).sort(), [groups])
  const coveredSet = useMemo(() => {
    const set = new Set(form.keywords.map((k) => k.trim().toLowerCase()))
    return set
  }, [form.keywords])
  const liveScore = allKeywords.length > 0 ? Math.round((coveredSet.size / allKeywords.length) * 100) : 0

  if (!open) return null

  function set<K extends keyof JobDraft>(key: K, value: JobDraft[K]) {
    setForm((f) => ({ ...f, [key]: value }))
  }

  function toggleKeyword(kw: string) {
    const k = kw.trim().toLowerCase()
    const next = form.keywords.includes(k)
      ? form.keywords.filter((x) => x !== k)
      : [...form.keywords, kw.trim()]
    set('keywords', next)
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const nextErrors: typeof errors = {}
    if (!form.company.trim()) nextErrors.company = 'Company name is required'
    if (!form.role.trim()) nextErrors.role = 'Job title / role is required'
    setErrors(nextErrors)
    if (Object.keys(nextErrors).length > 0) return

    const url = form.url.trim()
    onSubmit(
      {
        ...form,
        company: form.company.trim(),
        role: form.role.trim(),
        url: url && !/^https?:\/\//i.test(url) ? `https://${url}` : url,
        resume: form.resume.trim(),
        salary: form.salary.trim(),
        notes: form.notes.trim(),
        dateApplied: normalizeDate(form.dateApplied),
        keywords: Array.from(new Set(form.keywords.map((k) => k.trim()).filter(Boolean))),
      },
      initial?.id,
    )
  }

  const showNewResumeInput =
    resumeMode === 'new' || (form.resume && !resumes.includes(form.resume))

  return (
    <div className="modal-backdrop" onMouseDown={onClose}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="job-modal-title"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <header className="modal__header">
          <div>
            <h2 id="job-modal-title">{initial ? 'Edit job' : 'Add job'}</h2>
            <p>{initial ? 'Update the details below.' : 'Track a new opportunity in your pipeline.'}</p>
          </div>
          <button type="button" className="icon-btn" aria-label="Close" onClick={onClose}>
            <X size={18} />
          </button>
        </header>

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-grid">
            <div className="field">
              <label htmlFor="company">Company name *</label>
              <input
                id="company"
                type="text"
                placeholder="e.g. Google"
                value={form.company}
                onChange={(e) => set('company', e.target.value)}
                className={errors.company ? 'invalid' : ''}
                autoFocus
              />
              {errors.company && <span className="field__error">{errors.company}</span>}
            </div>

            <div className="field">
              <label htmlFor="role">Job title / role *</label>
              <input
                id="role"
                type="text"
                placeholder="e.g. SDET Engineer II"
                value={form.role}
                onChange={(e) => set('role', e.target.value)}
                className={errors.role ? 'invalid' : ''}
              />
              {errors.role && <span className="field__error">{errors.role}</span>}
            </div>

            <div className="field field--wide">
              <label htmlFor="url">LinkedIn job URL</label>
              <input
                id="url"
                type="url"
                placeholder="https://www.linkedin.com/jobs/view/…"
                value={form.url}
                onChange={(e) => set('url', e.target.value)}
              />
            </div>

            <div className="field field--wide">
              <label>Resume used</label>
              {resumes.length > 0 && (
                <div className="segmented">
                  <button
                    type="button"
                    className={resumeMode === 'existing' ? 'active' : ''}
                    onClick={() => setResumeMode('existing')}
                  >
                    Pick saved
                  </button>
                  <button
                    type="button"
                    className={resumeMode === 'new' ? 'active' : ''}
                    onClick={() => setResumeMode('new')}
                  >
                    New name
                  </button>
                </div>
              )}
              {showNewResumeInput ? (
                <input
                  type="text"
                  placeholder='e.g. "SDE_Resume_v3" or "QA_Lead_Resume"'
                  value={form.resume}
                  onChange={(e) => set('resume', e.target.value)}
                  list="resume-options"
                />
              ) : (
                <select
                  value={form.resume}
                  onChange={(e) => set('resume', e.target.value)}
                >
                  <option value="">Select a resume…</option>
                  {resumes.map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              )}
              <datalist id="resume-options">
                {resumes.map((r) => (
                  <option key={r} value={r} />
                ))}
              </datalist>
            </div>

            <div className="field">
              <label htmlFor="dateApplied">Date applied</label>
              <input
                id="dateApplied"
                type="date"
                value={form.dateApplied}
                onChange={(e) => set('dateApplied', e.target.value)}
              />
            </div>

            <div className="field">
              <label htmlFor="salary">Salary range</label>
              <input
                id="salary"
                type="text"
                placeholder="e.g. ₹25–30 LPA or $150–180K"
                value={form.salary}
                onChange={(e) => set('salary', e.target.value)}
              />
            </div>

            <div className="field field--wide">
              <label htmlFor="status">Status</label>
              <select
                id="status"
                value={form.status}
                onChange={(e) => set('status', e.target.value as JobStatus)}
              >
                {COLUMNS.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.title} — {c.subtitle}
                  </option>
                ))}
              </select>
            </div>

            {/* ATS keyword coverage editor */}
            <div className="field field--wide ats-block">
              <div className="ats-block__head">
                <label>
                  <Scan size={14} />
                  ATS keyword coverage
                </label>
                <span className={`ats-pill ats-pill--${liveScore >= 75 ? 'good' : liveScore >= 45 ? 'ok' : 'bad'}`}>
                  {liveScore}% — {coveredSet.size}/{allKeywords.length}
                </span>
              </div>
              <p className="ats-block__hint">
                Tap keywords you cover for this role. This drives the ATS score on the board and in the Analyzer.
              </p>
              <div className="keyword-cloud">
                {allKeywords.map((kw) => {
                  const active = coveredSet.has(kw.toLowerCase())
                  return (
                    <button
                      key={kw}
                      type="button"
                      className={`kw-chip ${active ? 'kw-chip--on' : ''}`}
                      onClick={() => toggleKeyword(kw)}
                    >
                      {kw}
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="field field--wide">
              <label htmlFor="notes">Notes</label>
              <textarea
                id="notes"
                rows={3}
                placeholder="Recruiter name, referral info, interview stage…"
                value={form.notes}
                onChange={(e) => set('notes', e.target.value)}
              />
            </div>
          </div>

          <footer className="modal__footer">
            <button type="button" className="btn btn--ghost" onClick={onClose}>
              Cancel
            </button>
            <button type="submit" className="btn btn--primary">
              {initial ? 'Save changes' : 'Add job'}
            </button>
          </footer>
        </form>
      </div>
    </div>
  )
}