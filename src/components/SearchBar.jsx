export default function SearchBar({ query, genre, genres = [], onChange }) {
  const handleChange = (field, value) => {
    onChange?.({ query, genre, [field]: value });
  };

  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex-1 flex items-center gap-2 rounded-full bg-zinc-900/80 px-4 py-2 ring-1 ring-zinc-800 focus-within:ring-primary">
        <span className="text-zinc-500">🔍</span>
        <input
          type="text"
          placeholder="Search for movies, actors, genres..."
          className="w-full bg-transparent text-sm outline-none placeholder:text-zinc-500"
          value={query}
          onChange={(e) => handleChange('query', e.target.value)}
        />
      </div>
      <div className="flex gap-2">
        <select
          value={genre || ''}
          onChange={(e) => handleChange('genre', e.target.value || null)}
          className="rounded-full bg-zinc-900/80 px-3 py-2 text-sm text-gray-200 ring-1 ring-zinc-800 focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">All Genres</option>
          {genres.map((g) => (
            <option key={g} value={g}>
              {g}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

