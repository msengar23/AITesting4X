import { useMemo, useState } from 'react'
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  closestCorners,
  useSensor,
  useSensors,
  type DragEndEvent,
  type DragStartEvent,
} from '@dnd-kit/core'
import type { Job, JobStatus } from '../types'
import { COLUMNS } from '../types'
import { Column } from './Column'
import { JobCard } from './JobCard'
import { jobCoverage } from '../lib/keywordLib'
import type { KeywordGroup } from '../types'

const ACCENTS: Record<JobStatus, string> = {
  wishlist: '#8b8fa3',
  applied: '#f97316',
  followup: '#10b981',
}

interface Props {
  jobs: Job[]
  groups: KeywordGroup[]
  onMove: (id: string, status: JobStatus) => void
  onAdd: (status: JobStatus) => void
  onEdit: (job: Job) => void
  onDelete: (job: Job) => void
}

export function Board({ jobs, groups, onMove, onAdd, onEdit, onDelete }: Props) {
  const [activeId, setActiveId] = useState<string | null>(null)
  const sensors = useSensors(
    useSensor(PointerSensor, { activationConstraint: { distance: 6 } }),
  )

  const grouped = useMemo(() => {
    const map: Record<JobStatus, Job[]> = { wishlist: [], applied: [], followup: [] }
    for (const job of jobs) {
      if (job.status in map) map[job.status].push(job)
    }
    return map
  }, [jobs])

  const activeJob = activeId ? jobs.find((j) => j.id === activeId) : undefined

  function handleDragStart(event: DragStartEvent) {
    setActiveId(String(event.active.id))
  }

  function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event
    setActiveId(null)
    if (!over) return

    const activeJobObj = jobs.find((j) => j.id === active.id)
    if (!activeJobObj) return

    const overId = String(over.id)

    // Dropped on a column: move the card into that column.
    if (COLUMNS.some((c) => c.id === overId)) {
      if (activeJobObj.status !== overId) {
        onMove(activeJobObj.id, overId as JobStatus)
      }
      return
    }

    // Dropped on another card: if it belongs to a different column, move.
    const overJob = jobs.find((j) => j.id === overId)
    if (!overJob) return
    if (activeJobObj.status !== overJob.status) {
      onMove(activeJobObj.id, overJob.status)
    }
  }

  return (
    <DndContext
      sensors={sensors}
      collisionDetection={closestCorners}
      onDragStart={handleDragStart}
      onDragEnd={handleDragEnd}
      onDragCancel={() => setActiveId(null)}
    >
      <div className="kanban">
        {COLUMNS.map((col) => (
          <Column
            key={col.id}
            id={col.id}
            title={col.title}
            subtitle={col.subtitle}
            jobs={grouped[col.id]}
            accent={ACCENTS[col.id]}
            groups={groups}
            onAdd={onAdd}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>

      <DragOverlay dropAnimation={null}>
        {activeJob ? (
          <JobCard
            job={activeJob}
            score={jobCoverage(activeJob.keywords, groups).score}
            onEdit={() => {}}
            onDelete={() => {}}
          />
        ) : null}
      </DragOverlay>
    </DndContext>
  )
}