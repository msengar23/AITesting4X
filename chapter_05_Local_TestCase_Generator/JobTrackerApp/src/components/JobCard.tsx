import { useSortable } from '@dnd-kit/sortable'
import { CSS } from '@dnd-kit/utilities'
import { format } from 'date-fns'
import {
  Calendar,
  ExternalLink,
  FileText,
  GripVertical,
  Pencil,
  Scan,
  Trash2,
} from 'lucide-react'
import type { Job } from '../types'
import { scoreBand } from '../lib/keywordLib'

interface Props {
  job: Job
  score: number
  onEdit: (job: Job) => void
  onDelete: (job: Job) => void
}

export function JobCard({ job, score, onEdit, onDelete }: Props) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: job.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  const companyInitial = job.company.trim().charAt(0).toUpperCase() || '?'
  const band = scoreBand(score)

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className={`job-card ${isDragging ? 'dragging' : ''}`}
    >
      <div className="job-card__top">
        <div className="job-card__avatar">{companyInitial}</div>
        <div className="job-card__headings">
          <h4 className="job-card__company">{job.company}</h4>
          <p className="job-card__role">{job.role}</p>
        </div>
        <span className={`ats-pill ats-pill--${band.tone}`} title="ATS keyword coverage">
          <Scan size={12} />
          {score}%
        </span>
        <GripVertical className="job-card__grip" size={16} />
      </div>

      <div className="job-card__meta">
        {job.dateApplied && (
          <span className="chip chip--date">
            <Calendar size={12} />
            {format(new Date(`${job.dateApplied}T00:00:00`), 'dd MMM yyyy')}
          </span>
        )}
        {job.salary && <span className="chip chip--salary">{job.salary}</span>}
        {job.resume && (
          <span className="chip chip--resume" title={`Resume: ${job.resume}`}>
            <FileText size={12} />
            {job.resume}
          </span>
        )}
      </div>

      {job.url && (
        <a
          className="job-card__link"
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
        >
          <ExternalLink size={13} />
          View on LinkedIn
        </a>
      )}

      {job.notes && (
        <p className="job-card__notes" title={job.notes}>
          {job.notes}
        </p>
      )}

      <div className="job-card__actions">
        <button
          type="button"
          className="icon-btn"
          aria-label="Edit job"
          title="Edit"
          onClick={(e) => {
            e.stopPropagation()
            onEdit(job)
          }}
        >
          <Pencil size={15} />
        </button>
        <button
          type="button"
          className="icon-btn icon-btn--danger"
          aria-label="Delete job"
          title="Delete"
          onClick={(e) => {
            e.stopPropagation()
            onDelete(job)
          }}
        >
          <Trash2 size={15} />
        </button>
      </div>
    </div>
  )
}