export default function SearchBar({ query, onChange }) {
  return (
    <input
      value={query}
      onChange={(event) => onChange(event.target.value)}
      placeholder="Search by title "
      aria-label="Search projects"
      className="w-full rounded-xl border border-slate-300 bg-slate-50 px-3 py-2 text-sm outline-none transition focus:border-blue-400 focus:bg-white sm:max-w-xs"
    />
  )
}
