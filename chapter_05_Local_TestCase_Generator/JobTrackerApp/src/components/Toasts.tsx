import { CheckCircle2, Info, Trash2 } from 'lucide-react'

export type ToastKind = 'success' | 'info' | 'danger'

export interface Toast {
  id: number
  kind: ToastKind
  message: string
}

const ICONS = {
  success: CheckCircle2,
  info: Info,
  danger: Trash2,
}

export function Toasts({ toasts }: { toasts: Toast[] }) {
  return (
    <div className="toasts" aria-live="polite">
      {toasts.map((t) => {
        const Icon = ICONS[t.kind]
        return (
          <div key={t.id} className={`toast toast--${t.kind}`}>
            <Icon size={16} />
            <span>{t.message}</span>
          </div>
        )
      })}
    </div>
  )
}