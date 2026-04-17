import client from './client'

export const getProjects = () => client.get('/projects/').then(r => r.data)
export const getProject = (id) => client.get(`/projects/${id}`).then(r => r.data)
export const createProject = (data) => client.post('/projects/', data).then(r => r.data)
export const updateProject = (id, data) => client.patch(`/projects/${id}`, data).then(r => r.data)
export const deleteProject = (id) => client.delete(`/projects/${id}`)

export const createTask = (projectId, data) => client.post(`/projects/${projectId}/tasks`, data).then(r => r.data)
export const updateTask = (projectId, taskId, data) => client.patch(`/projects/${projectId}/tasks/${taskId}`, data).then(r => r.data)
export const deleteTask = (projectId, taskId) => client.delete(`/projects/${projectId}/tasks/${taskId}`)
