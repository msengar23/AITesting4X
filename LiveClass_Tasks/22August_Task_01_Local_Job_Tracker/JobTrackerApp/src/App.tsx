import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { Job, JobDraft, JobStatus } from './types'
import { COLUMNS } from './types'
import { useJobs } from './lib/useJobs'
import { jobCoverage } from './lib/keywordLib'
import { Sidebar } from './components/Sidebar'
import { TopBar } from './components/TopBar'
import { Hero } from './components/Hero'
import { Board } from './components/Board'
import { JobModal } from './components/JobModal'
import { Toasts, type Toast, type ToastKind } from './components/Toasts'

const USER_NAME = 'Mamta Singh'

export default function App() {
  const { jobs, groups, loading, counts, resumes, create, update, remove, move } = useJobs()

  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem('jobtracker-theme')
    if (saved) return saved === 'dark'
    return window.matchMedia?.('(prefers-color-scheme: dark)').matches ?? false
  })
  const [search, setSearch] = useState('')
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<Job | null>(null)
  const [modalStatus, setModalStatus] = useState<JobStatus>('wishlist')
  const [toasts, setToasts] = useState<Toast[]>([])
  const toastId = useRef(0)

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? 'dark' : 'light'
    localStorage.setItem('jobtracker-theme', dark ? 'dark' : 'light')
  }, [dark])

  const pushToast = useCallback((message: string, kind: ToastKind = 'success') => {
    const id = ++toastId.current
    setToasts((prev) => [...prev, { id, kind, message }])
    window.setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, 2800)
  }, [])

  const openCreate = useCallback((status: JobStatus = 'wishlist') => {
    setEditing(null)
    setModalStatus(status)
    setModalOpen(true)
  }, [])

  const openEdit = useCallback((job: Job) => {
    setEditing(job)
    setModalStatus(job.status)
    setModalOpen(true)
  }, [])

  const handleSubmit = useCallback(
    async (draft: JobDraft, id?: string) => {
      try {
        if (id) {
          const existing = jobs.find((j) => j.id === id)
          if (existing) await update({ ...existing, ...draft })
          pushToast(`Updated ${draft.company} job`)
        } else {
          await create(draft)
          pushToast(`Added ${draft.company} to ${COLUMNS.find((c) => c.id === draft.status)?.title}`)
        }
        setModalOpen(false)
        setEditing(null)
      } catch (err) {
        console.error(err)
        pushToast('Could not save the job', 'danger')
      }
    },
    [jobs, create, update, pushToast],
  )

  const handleDelete = useCallback(
    async (job: Job) => {
      if (!window.confirm(`Delete the ${job.company} — ${job.role} job?`)) return
      try {
        await remove(job.id)
        pushToast(`Deleted ${job.company} job`, 'info')
      } catch (err) {
        console.error(err)
        pushToast('Could not delete the job', 'danger')
      }
    },
    [remove, pushToast],
  )

  const handleMove = useCallback(
    async (id: string, status: JobStatus) => {
      try {
        await move(id, status)
        pushToast(`Moved to ${COLUMNS.find((c) => c.id === status)?.title}`)
      } catch (err) {
        console.error(err)
        pushToast('Could not move the job', 'danger')
      }
    },
    [move, pushToast],
  )

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase()
    if (!q) return jobs
    return jobs.filter(
      (j) => j.company.toLowerCase().includes(q) || j.role.toLowerCase().includes(q),
    )
  }, [jobs, search])

  // Aggregate ATS keyword coverage across all tracked keywords.
  const ats = useMemo(() => {
    if (jobs.length === 0) {
      return { score: 0, matched: [], missing: [], foundCount: 0, totalCount: 0 }
    }
    const covered = new Set<string>()
    for (const job of jobs) {
      for (const kw of job.keywords) covered.add(kw.trim().toLowerCase())
    }
    return jobCoverage(Array.from(covered), groups)
  }, [jobs, groups])

  return (
    <div className="app">
      <Sidebar collapsed={sidebarCollapsed} onToggle={() => setSidebarCollapsed((c) => !c)} />

      <main className="main">
        <TopBar
          search={search}
          onSearch={setSearch}
          dark={dark}
          onToggleTheme={() => setDark((d) => !d)}
          onAdd={() => openCreate('wishlist')}
        />

        <div className="main__content">
          <Hero counts={counts} name={USER_NAME} ats={ats} />

          {loading ? (
            <div className="board-loading">
              <span className="spinner" />
              Loading your jobs…
            </div>
          ) : (
            <Board
              jobs={filtered}
              groups={groups}
              onMove={handleMove}
              onAdd={(status) => openCreate(status)}
              onEdit={openEdit}
              onDelete={handleDelete}
            />
          )}
        </div>
      </main>

      <JobModal
        key={modalOpen ? (editing?.id ?? `new-${modalStatus}`) : 'closed'}
        open={modalOpen}
        initial={editing}
        status={modalStatus}
        resumes={resumes}
        groups={groups}
        onClose={() => {
          setModalOpen(false)
          setEditing(null)
        }}
        onSubmit={handleSubmit}
      />

      <Toasts toasts={toasts} />
    </div>
  )
}