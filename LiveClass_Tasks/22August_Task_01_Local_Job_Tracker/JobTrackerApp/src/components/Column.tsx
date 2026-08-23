import { useDroppable } from '@dnd-kit/core'
import {
  SortableContext,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable'
import { Plus } from 'lucide-react'
import type { Job, JobStatus, KeywordGroup } from '../types'
import { JobCard } from './JobCard'
import { jobCoverage } from '../lib/keywordLib'

interface Props {
  id: JobStatus
  title: string
  subtitle: string
  jobs: Job[]
  accent: string
  groups: KeywordGroup[]
  onAdd: (status: JobStatus) => void
  onEdit: (job: Job) => void
  onDelete: (job: Job) => void
}

export function Column({
  id,
  title,
  subtitle,
  jobs,
  accent,
  groups,
  onAdd,
  onEdit,
  onDelete,
}: Props) {
  const { setNodeRef, isOver } = useDroppable({ id })

  const scores = jobs.map((job) => ({
    job,
    score: jobCoverage(job.keywords, groups).score,
  }))

  return (
    <section
      ref={setNodeRef}
      className={`kanban-col ${isOver ? 'kanban-col--over' : ''}`}
    >
      <header className="kanban-col__header">
        <div className="kanban-col__title">
          <span className="kanban-col__dot" style={{ background: accent }} />
          <h3>{title}</h3>
          <span className="kanban-col__count">{jobs.length}</span>
        </div>
        <p className="kanban-col__subtitle">{subtitle}</p>
        <button type="button" className="kanban-col__add" onClick={() => onAdd(id)}>
          <Plus size={15} />
          Add job
        </button>
      </header>

      <SortableContext
        items={jobs.map((j) => j.id)}
        strategy={verticalListSortingStrategy}
      >
        <div className="kanban-col__body">
          {scores.map(({ job, score }) => (
            <JobCard
              key={job.id}
              job={job}
              score={score}
              onEdit={onEdit}
              onDelete={onDelete}
            />
          ))}
          {jobs.length === 0 && (
            <div className="kanban-col__empty">
              <span>No jobs yet</span>
              <p>Drop a card here or add one.</p>
            </div>
          )}
        </div>
      </SortableContext>
    </section>
  )
}