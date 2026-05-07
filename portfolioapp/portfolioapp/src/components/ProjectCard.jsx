export default function ProjectCard({ project }) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="text-base font-semibold text-slate-900">{project.title}</h3>
      <p className="mt-2 text-sm leading-relaxed text-slate-600">{project.description}</p>
    </article>
  )
}
