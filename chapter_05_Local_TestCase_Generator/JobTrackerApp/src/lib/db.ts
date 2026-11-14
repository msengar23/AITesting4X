import { openDB, type DBSchema, type IDBPDatabase } from 'idb'
import type { Job, KeywordGroup } from '../types'
import { uid } from './uid'

interface JobTrackerDB extends DBSchema {
  jobs: {
    key: string
    value: Job
    indexes: {
      'by-status': Job['status']
      'by-date': Job['dateApplied']
    }
  }
  keywords: {
    key: string
    value: KeywordGroup
  }
}

const DB_NAME = 'job-tracker-ats-db'
const DB_VERSION = 1
const STORE_JOBS = 'jobs'
const STORE_KEYWORDS = 'keywords'

let dbPromise: Promise<IDBPDatabase<JobTrackerDB>> | null = null

function getDB(): Promise<IDBPDatabase<JobTrackerDB>> {
  if (!dbPromise) {
    dbPromise = openDB<JobTrackerDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains(STORE_JOBS)) {
          const store = db.createObjectStore(STORE_JOBS, { keyPath: 'id' })
          store.createIndex('by-status', 'status')
          store.createIndex('by-date', 'dateApplied')
        }
        if (!db.objectStoreNames.contains(STORE_KEYWORDS)) {
          db.createObjectStore(STORE_KEYWORDS, { keyPath: 'id' })
        }
      },
    })
  }
  return dbPromise
}

// ---- Jobs ----
export async function getAllJobs(): Promise<Job[]> {
  const db = await getDB()
  return db.getAll(STORE_JOBS)
}

export async function addJob(job: Job): Promise<void> {
  const db = await getDB()
  await db.add(STORE_JOBS, job)
}

export async function putJob(job: Job): Promise<void> {
  const db = await getDB()
  await db.put(STORE_JOBS, job)
}

export async function deleteJob(id: string): Promise<void> {
  const db = await getDB()
  await db.delete(STORE_JOBS, id)
}

// ---- Keywords ----
export async function getKeywords(): Promise<KeywordGroup[]> {
  const db = await getDB()
  return db.getAll(STORE_KEYWORDS)
}

export async function putGroups(groups: KeywordGroup[]): Promise<void> {
  const db = await getDB()
  const tx = db.transaction(STORE_KEYWORDS, 'readwrite')
  await Promise.all(
    groups.map((g) => {
      tx.store.delete(g.id)
      return tx.store.add(g)
    }),
  )
  await tx.done
}

/** Seed sample data only when the store is empty (first run). */
export async function seedIfEmpty(
  seedGroups: KeywordGroup[],
): Promise<void> {
  const db = await getDB()
  const count = await db.count(STORE_JOBS)

  const kwCount = await db.count(STORE_KEYWORDS)
  if (kwCount === 0) {
    const tx = db.transaction(STORE_KEYWORDS, 'readwrite')
    await Promise.all(seedGroups.map((g) => tx.store.add(g)))
    await tx.done
  }

  if (count > 0) return

  const today = new Date()
  const daysAgo = (n: number) => {
    const d = new Date(today)
    d.setDate(d.getDate() - n)
    return d.toISOString().slice(0, 10)
  }

  const seed: Job[] = [
    {
      id: uid(),
      company: 'Google',
      role: 'SDET Engineer II',
      url: 'https://www.linkedin.com/jobs/view/sdet-google',
      resume: 'QA_SDET_Resume_v2',
      dateApplied: daysAgo(1),
      salary: '₹35–45 LPA',
      notes: 'Referred by Priya (SDE3). Recruiter: Sarah — first round this week.',
      status: 'applied',
      keywords: ['playwright', 'selenium', 'java', 'api testing', 'ci/cd'],
      missingKeywords: ['load testing', 'kubernetes', 'aws'],
      jdText: '',
      createdAt: Date.now() - 86400000,
    },
    {
      id: uid(),
      company: 'Microsoft',
      role: 'Senior QA Engineer',
      url: 'https://www.linkedin.com/jobs/view/senior-qa-microsoft',
      resume: 'QA_SDET_Resume_v2',
      dateApplied: daysAgo(4),
      salary: '$150–180K',
      notes: 'Hiring manager: David. Asked for API automation samples.',
      status: 'followup',
      keywords: ['rest assured', 'testing', 'sql', 'azure pipelines'],
      missingKeywords: ['kubernetes', 'performance testing'],
      jdText: '',
      createdAt: Date.now() - 4 * 86400000,
    },
    {
      id: uid(),
      company: 'Atlassian',
      role: 'QA Automation Engineer',
      url: 'https://www.linkedin.com/jobs/view/qa-automation-atlassian',
      resume: 'QA_Lead_Resume',
      dateApplied: daysAgo(0),
      salary: '₹28–35 LPA',
      notes: '',
      status: 'wishlist',
      keywords: ['cypress', 'javascript', 'agile'],
      missingKeywords: ['docker', 'api automation', 'load testing'],
      jdText: '',
      createdAt: Date.now(),
    },
    {
      id: uid(),
      company: 'Adobe',
      role: 'SDET (Web SDK)',
      url: 'https://www.linkedin.com/jobs/view/sdet-web-sdk-adobe',
      resume: 'SDE_Resume_v3',
      dateApplied: daysAgo(9),
      salary: '$130–160K',
      notes: 'Referred by Ankit. OA scheduled.',
      status: 'applied',
      keywords: ['javascript', 'typescript', 'playwright', 'github actions'],
      missingKeywords: ['security testing', 'mobile testing'],
      jdText: '',
      createdAt: Date.now() - 9 * 86400000,
    },
  ]

  const tx = db.transaction(STORE_JOBS, 'readwrite')
  await Promise.all(seed.map((job) => tx.store.add(job)))
  await tx.done
}