import { useMemo, useState } from 'react'
import ProjectForm from './components/ProjectForm'
import ProjectGallery from './components/ProjectGallery'

const starterProjects = [
  {
    id: 1,
    title: 'Budget planner',
    description: 'A simple expense tracker with category charts and monthly summaries.',
  },
  {
    id: 2,
    title: 'Study planner',
    description: 'A focused timer app with tasks and streak tracking for study sessions.',
  },
  {
    id: 3,
    title: 'Recipe Maker',
    description: 'Search and save favorite recipes with tags and difficulty filters.',
  },
]

export default function App() {
  const [projects, setProjects] = useState(starterProjects)
  const [query, setQuery] = useState('')

  const filteredProjects = useMemo(() => {
    const searchText = query.trim().toLowerCase()
    if (!searchText) return projects
    return projects.filter(({ title, description }) =>
      `${title} ${description}`.toLowerCase().includes(searchText)
    )
  }, [projects, query])

  function handleAddProject({ title, description }) {
    setProjects((prev) => [{ id: Date.now(), title, description }, ...prev])
  }

  return (
    <div className="min-h-screen bg-blue-50 text-slate-800">
      <header className="border-b border-slate-200 bg-white px-4 py-4 sm:px-8">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <h1 className="text-xl font-bold tracking-tight text-slate-900">
            My Project Showcase
          </h1>
        </div>
      </header>

      <main className="mx-auto w-full max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-5">
          <div className="lg:col-span-2">
            <ProjectForm onAdd={handleAddProject} />
          </div>
          <div className="lg:col-span-3">
            <ProjectGallery
              projects={filteredProjects}
              query={query}
              onQueryChange={setQuery}
            />
          </div>
        </div>
      </main>
    </div>
  )
}
