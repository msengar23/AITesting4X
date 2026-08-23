import { Moon, Plus, Search, Sun } from 'lucide-react'

interface Props {
  search: string
  onSearch: (value: string) => void
  dark: boolean
  onToggleTheme: () => void
  onAdd: () => void
}

export function TopBar({ search, onSearch, dark, onToggleTheme, onAdd }: Props) {
  return (
    <header className="topbar">
      <div className="topbar__search">
        <Search size={16} />
        <input
          type="search"
          placeholder="Search by company or role…"
          value={search}
          onChange={(e) => onSearch(e.target.value)}
          aria-label="Search jobs"
        />
      </div>

      <div className="topbar__actions">
        <button
          type="button"
          className="icon-btn"
          aria-label="Toggle theme"
          title={dark ? 'Switch to light mode' : 'Switch to dark mode'}
          onClick={onToggleTheme}
        >
          {dark ? <Sun size={18} /> : <Moon size={18} />}
        </button>
        <button type="button" className="btn btn--primary" onClick={onAdd}>
          <Plus size={16} />
          Add job
        </button>
      </div>
    </header>
  )
}