import MovieCard from './MovieCard.jsx';

export default function RecommendationList({ title, movies }) {
  if (!movies || movies.length === 0) return null;

  return (
    <section className="space-y-3">
      <h2 className="text-lg font-semibold text-white">{title}</h2>
      <div className="flex gap-4 overflow-x-auto pb-2">
        {movies.map((movie) => (
          <div key={movie.id} className="min-w-[140px] max-w-[160px]">
            <MovieCard movie={movie} />
          </div>
        ))}
      </div>
    </section>
  );
}

