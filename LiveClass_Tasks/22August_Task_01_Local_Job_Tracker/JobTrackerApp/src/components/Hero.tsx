import { Briefcase, ClipboardList, Sparkles, Target, TrendingUp } from 'lucide-react'
import type { JobStatus } from '../types'
import { COLUMNS } from '../types'
import type { AtsResult } from '../types'

interface Props {
  counts: Record<JobStatus, number> & { total: number }
  name: string
  ats: AtsResult
}

export function Hero({ counts, name, ats }: Props) {
  const appliedRatio = counts.total > 0 ? Math.round((counts.applied / counts.total) * 100) : 0
  const followUpRatio = counts.total > 0 ? Math.round((counts.followup / counts.total) * 100) : 0

  return (
    <>
      <section className="hero">
        <div className="hero__main">
          <span className="hero__badge">
            <Sparkles size={14} />
            QA/SDET Job Tracker
          </span>
          <h1>Turn a saved role into a follow-up, one board at a time.</h1>
          <p>
            {name}, track every application in one local-first board — drag cards from
            Wishlist &rarr; Applied &rarr; Follow-up. Use the ATS Analyzer to cover the
            right keywords on each JD. Everything stays in your browser.
          </p>
          <div className="hero__cta">
            <span className="hero__stat">
              <strong>{counts.total}</strong> jobs tracked
            </span>
            <span className="hero__stat">
              <strong>{counts.applied}</strong> applications
            </span>
            <span className="hero__stat">
              <strong>{counts.followup}</strong> follow-ups
            </span>
          </div>
        </div>

        <div className="hero__readiness">
          <div className="hero__readiness-head">
            <ClipboardList size={16} />
            ATS keyword coverage
          </div>
          <div className="hero__readiness-percent">{ats.score}%</div>
          <div className="progress">
            <div className="progress__bar" style={{ width: `${Math.max(ats.score, 4)}%` }} />
          </div>
          <div className="hero__readiness-rows">
            <div className="readiness-row">
              <span>Keywords covered</span>
              <span className="status-no">{ats.foundCount}/{ats.totalCount}</span>
            </div>
            {ats.missing.length > 0 && (
              <div className="readiness-row">
                <span>Missing</span>
                <span className="status-cta">{ats.missing.length}</span>
              </div>
            )}
            <div className="readiness-row">
              <span>Applications</span>
              <span className="status-cta">{appliedRatio}%</span>
            </div>
            <div className="readiness-row">
              <span>Followed up</span>
              <span className="status-no">{followUpRatio}%</span>
            </div>
          </div>
        </div>
      </section>

      <section className="stat-cards">
        {COLUMNS.map((col, i) => {
          const Icon = [Briefcase, TrendingUp, Target][i]
          const accent = ['#8b8fa3', '#f97316', '#10b981'][i]
          return (
            <div key={col.id} className="stat-card">
              <div className="stat-card__icon" style={{ background: `${accent}1a`, color: accent }}>
                <Icon size={20} />
              </div>
              <div>
                <p>{col.title}</p>
                <h3>{counts[col.id]}</h3>
              </div>
            </div>
          )
        })}
      </section>
    </>
  )
}