import { NavLink } from 'react-router-dom'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: '📊' },
  { to: '/routines', label: 'Routines', icon: '✅' },
  { to: '/projects', label: 'Projects', icon: '📁' },
  { to: '/chat', label: 'AI Chat', icon: '🤖' },
]

export default function Sidebar() {
  return (
    <aside className="w-56 min-h-screen bg-gray-900 border-r border-gray-800 flex flex-col py-6 px-3">
      <div className="text-white font-bold text-xl px-3 mb-8">LifeStack</div>
      <nav className="flex flex-col gap-1">
        {links.map(({ to, label, icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                isActive
                  ? 'bg-indigo-600 text-white'
                  : 'text-gray-400 hover:text-white hover:bg-gray-800'
              }`
            }
          >
            <span>{icon}</span>
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
