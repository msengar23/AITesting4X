import { Briefcase, ChevronLeft } from 'lucide-react'

export function Sidebar({
  collapsed,
  onToggle,
}: {
  collapsed: boolean
  onToggle: () => void
}) {
  return (
    <aside className={`sidebar ${collapsed ? 'sidebar--collapsed' : ''}`}>
      <div className="sidebar__brand">
        <div className="brand-mark">
          <Briefcase size={18} />
        </div>
        {!collapsed && <span className="brand-name">Job Tracker</span>}
        <button
          type="button"
          className="sidebar__collapse"
          aria-label="Toggle sidebar"
          onClick={onToggle}
        >
          <ChevronLeft size={16} />
        </button>
      </div>

      {!collapsed && (
        <nav className="sidebar__nav">
          <a href="#" className="sidebar__link active" onClick={(e) => e.preventDefault()}>
            <Briefcase size={17} />
            <span>Job Tracker</span>
          </a>
        </nav>
      )}
    </aside>
  )
}