import { useNavigate } from 'react-router-dom';
import RatingStars from './RatingStars.jsx';

export default function MovieCard({ movie }) {
  const navigate = useNavigate();

  const handleClick = () => {
    if (!movie?.id) return;
    navigate(`/movie/${movie.id}`);
  };

  return (
    <div
      className="group relative cursor-pointer overflow-hidden rounded-xl bg-zinc-900/60 shadow-lg shadow-black/40 transition hover:-translate-y-1 hover:shadow-2xl"
      onClick={handleClick}
    >
      <div className="aspect-[2/3] w-full overflow-hidden bg-zinc-800">
        {movie?.posterUrl ? (
          <img
            src={movie.posterUrl}
            alt={movie.title}
            className="h-full w-full object-cover transition duration-500 group-hover:scale-105 group-hover:opacity-80"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-gray-500">
            No poster
          </div>
        )}
      </div>
      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent opacity-70 group-hover:opacity-90 transition" />
      <div className="absolute inset-x-0 bottom-0 p-3 space-y-1">
        <h3 className="line-clamp-1 text-sm font-semibold text-white">
          {movie?.title ?? 'Untitled'}
        </h3>
        <div className="flex items-center justify-between gap-2">
          <RatingStars value={movie?.rating ?? 0} readOnly size="sm" />
          {movie?.genres && (
            <p className="line-clamp-1 text-[11px] text-gray-400">
              {Array.isArray(movie.genres) ? movie.genres.join(' • ') : movie.genres}
            </p>
          )}
        </div>
        <button
          type="button"
          className="mt-2 w-full rounded-full bg-primary py-1.5 text-xs font-medium text-white opacity-0 group-hover:opacity-100 transition"
        >
          View Details
        </button>
      </div>
    </div>
  );
}

