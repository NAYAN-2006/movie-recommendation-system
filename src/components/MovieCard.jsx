import { useNavigate } from 'react-router-dom';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import RatingStars from './RatingStars.jsx';
import { getMoviePoster, getMovieRating } from '../utils/movieHelpers.js';

export default function MovieCard({ movie }) {
  const navigate = useNavigate();
  const movieId = movie?.id ?? movie?.movie_id;
  const rating = Math.min(5, Math.max(0, getMovieRating(movie)));

  const handleViewDetails = (e) => {
    e.stopPropagation();
    if (!movieId) return;
    navigate(`/movie/${movieId}`);
  };

  const handleWatchlist = (e) => {
    e.stopPropagation();
    // Placeholder: integrate with watchlist backend when available
    window.alert(`Added "${movie?.title ?? 'this movie'}" to your watchlist.`);
  };

  const posterSrc = getMoviePoster(movie);

  return (
    <motion.div
      className="group relative cursor-pointer overflow-hidden rounded-2xl bg-zinc-900/40 ring-1 ring-white/10 shadow-lg shadow-black/40"
      whileHover={{ scale: 1.08, y: -8 }}
      transition={{ type: 'spring', stiffness: 280, damping: 20 }}
      onClick={handleViewDetails}
    >
      <div className="aspect-[2/3] w-full overflow-hidden bg-zinc-900">
        <img
          src={posterSrc}
          alt={movie?.title ?? 'Movie poster'}
          loading="lazy"
          className="h-full w-full object-cover transition duration-500 group-hover:scale-105 group-hover:opacity-90"
        />
      </div>

      <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent opacity-0 group-hover:opacity-100 transition" />

      <div className="absolute inset-0 flex flex-col justify-between p-3 opacity-0 group-hover:opacity-100 transition duration-300">
        <div className="flex items-start justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-black/60 px-3 py-1 text-xs font-semibold text-white backdrop-blur">
              ⭐ {rating.toFixed(1)}
            </span>
            <RatingStars value={rating} readOnly size="sm" />
          </div>
          <span className="rounded-full bg-black/60 px-3 py-1 text-xs font-semibold text-white backdrop-blur">
            {movie?.release_year ?? movie?.year ?? ''}
          </span>
        </div>

        <div className="space-y-2">
          <h3 className="line-clamp-2 text-sm font-semibold text-white">
            {movie?.title ?? 'Untitled'}
          </h3>
          <div className="flex flex-wrap gap-2">
            <motion.button
              type="button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex-1 rounded-full bg-primary px-3 py-2 text-xs font-semibold text-white shadow-lg shadow-red-500/30 transition"
              onClick={handleViewDetails}
            >
              View Details
            </motion.button>
            <motion.button
              type="button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex-1 rounded-full border border-white/20 bg-white/10 px-3 py-2 text-xs font-semibold text-white transition"
              onClick={handleWatchlist}
            >
              + Watchlist
            </motion.button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

