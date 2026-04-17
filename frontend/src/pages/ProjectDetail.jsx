import { useParams } from 'react-router-dom'

export default function ProjectDetail() {
  const { id } = useParams()
  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold text-white mb-2">Project #{id}</h1>
      <p className="text-gray-400">Tasks and AI panel — coming soon</p>
    </div>
  )
}
