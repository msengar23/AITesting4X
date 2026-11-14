import { useCallback, useEffect, useMemo, useState } from 'react'
import type { Job, JobDraft, JobStatus, KeywordGroup } from '../types'
import {
  addJob,
  deleteJob,
  getAllJobs,
  getKeywords,
  putGroups,
  putJob,
  seedIfEmpty,
} from './db'
import { uid } from './uid'
import { DEFAULT_KEYWORD_GROUPS } from './keywordLib'

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [groups, setGroups] = useState<KeywordGroup[]>(DEFAULT_KEYWORD_GROUPS)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    ;(async () => {
      // Seed DB with the default keyword library + sample jobs (first run only).
      await seedIfEmpty(DEFAULT_KEYWORD_GROUPS)
      const [all, keywordGroups] = await Promise.all([getAllJobs(), getKeywords()])
      if (active) {
        if (keywordGroups.length > 0) setGroups(keywordGroups)
        setJobs(all)
        setLoading(false)
      }
    })().catch((err) => {
      console.error('Failed to load data from IndexedDB:', err)
      if (active) setLoading(false)
    })
    return () => {
      active = false
    }
  }, [])

  const create = useCallback(async (draft: JobDraft): Promise<Job> => {
    const job: Job = {
      ...draft,
      id: uid(),
      createdAt: Date.now(),
    }
    await addJob(job)
    setJobs((prev) => [job, ...prev])
    return job
  }, [])

  const update = useCallback(async (job: Job): Promise<void> => {
    await putJob(job)
    setJobs((prev) => prev.map((j) => (j.id === job.id ? job : j)))
  }, [])

  const remove = useCallback(async (id: string): Promise<void> => {
    await deleteJob(id)
    setJobs((prev) => prev.filter((j) => j.id !== id))
  }, [])

  const move = useCallback(
    async (id: string, status: JobStatus): Promise<void> => {
      setJobs((prev) =>
        prev.map((j) => (j.id === id ? { ...j, status } : j)),
      )
      // Persist after optimistic update.
      const target = jobs.find((j) => j.id === id)
      if (target) await putJob({ ...target, status })
    },
    [jobs],
  )

  const saveGroups = useCallback(async (next: KeywordGroup[]): Promise<void> => {
    setGroups(next)
    await putGroups(next)
  }, [])

  const resumes = useMemo(() => {
    const names = new Set(jobs.map((j) => j.resume.trim()).filter(Boolean))
    return Array.from(names).sort((a, b) => a.localeCompare(b))
  }, [jobs])

  const counts = useMemo(
    () => ({
      wishlist: jobs.filter((j) => j.status === 'wishlist').length,
      applied: jobs.filter((j) => j.status === 'applied').length,
      followup: jobs.filter((j) => j.status === 'followup').length,
      total: jobs.length,
    }),
    [jobs],
  )

  return {
    jobs,
    groups,
    loading,
    counts,
    resumes,
    create,
    update,
    remove,
    move,
    saveGroups,
  }
}

export type UseJobs = ReturnType<typeof useJobs>