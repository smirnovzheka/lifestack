import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getProjects, createProject, deleteProject } from '../api/projects'

const CATEGORIES = ['work', 'pet_project', 'health', 'personal', 'finance']
const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4']

export default function Projects() {
  const [projects, setProjects] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', description: '', category: 'work', color: '#6366f1' })
  const navigate = useNavigate()

  useEffect(() => {
    getProjects().then(setProjects)
  }, [])

  async function handleCreate(e) {
    e.preventDefault()
    const project = await createProject(form)
    setProjects(prev => [project, ...prev])
    setShowForm(false)
    setForm({ name: '', description: '', category: 'work', color: '#6366f1' })
  }

  async function handleDelete(e, id) {
    e.stopPropagation()
    await deleteProject(id)
    setProjects(prev => prev.filter(p => p.id !== id))
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-white">Projects</h1>
        <button
          onClick={() => setShowForm(true)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg transition-colors"
        >
          + New project
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-gray-900 border border-gray-800 rounded-xl p-5 mb-6 flex flex-col gap-3">
          <input
            className="bg-gray-800 text-white px-3 py-2 rounded-lg text-sm outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Project name"
            value={form.name}
            onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            required
          />
          <input
            className="bg-gray-800 text-white px-3 py-2 rounded-lg text-sm outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="Description (optional)"
            value={form.description}
            onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
          />
          <select
            className="bg-gray-800 text-white px-3 py-2 rounded-lg text-sm outline-none focus:ring-1 focus:ring-indigo-500"
            value={form.category}
            onChange={e => setForm(f => ({ ...f, category: e.target.value }))}
          >
            {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
          <div className="flex gap-2">
            {COLORS.map(c => (
              <button
                key={c}
                type="button"
                onClick={() => setForm(f => ({ ...f, color: c }))}
                className={`w-6 h-6 rounded-full border-2 transition-all ${form.color === c ? 'border-white scale-110' : 'border-transparent'}`}
                style={{ backgroundColor: c }}
              />
            ))}
          </div>
          <div className="flex gap-2">
            <button type="submit" className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg">Create</button>
            <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg">Cancel</button>
          </div>
        </form>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {projects.map(p => (
          <div
            key={p.id}
            onClick={() => navigate(`/projects/${p.id}`)}
            className="bg-gray-900 border border-gray-800 rounded-xl p-5 cursor-pointer hover:border-gray-600 transition-colors group"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: p.color }} />
                <span className="text-white font-medium">{p.name}</span>
              </div>
              <button
                onClick={e => handleDelete(e, p.id)}
                className="text-gray-600 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all text-sm"
              >
                ✕
              </button>
            </div>
            {p.description && <p className="text-gray-400 text-sm mb-3 line-clamp-2">{p.description}</p>}
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500 bg-gray-800 px-2 py-1 rounded">{p.category}</span>
              <span className="text-xs text-gray-500">{p.tasks_done}/{p.tasks_total} tasks</span>
            </div>
            {p.tasks_total > 0 && (
              <div className="mt-3 h-1 bg-gray-800 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{ width: `${Math.round(p.tasks_done / p.tasks_total * 100)}%`, backgroundColor: p.color }}
                />
              </div>
            )}
          </div>
        ))}
        {projects.length === 0 && (
          <p className="text-gray-500 text-sm col-span-3">No projects yet. Create your first one!</p>
        )}
      </div>
    </div>
  )
}
