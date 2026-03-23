// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import MovieCard from './MovieCard.jsx';
import SkeletonMovieCard from './SkeletonMovieCard.jsx';

export default function MovieRow({ title, movies = [], loading = false, emptyMessage }) {
  const showEmpty = !loading && (!movies || movies.length === 0);

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white sm:text-xl">{title}</h2>
        {showEmpty && emptyMessage && (
          <p className="text-sm text-gray-400">{emptyMessage}</p>
        )}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'easeOut' }}
        className="relative"
      >
        <div className="flex snap-x snap-mandatory gap-4 overflow-x-auto pb-2 pr-2 scroll-smooth">
          {loading
            ? Array.from({ length: 6 }).map((_, idx) => (
                <div key={idx} className="min-w-[160px] max-w-[160px] snap-start">
                  <SkeletonMovieCard />
                </div>
              ))
            : movies.map((movie) => (
                <div key={movie.id ?? movie.movie_id} className="min-w-[160px] max-w-[160px] snap-start">
                  <MovieCard movie={movie} />
                </div>
              ))}
        </div>
      </motion.div>

      {showEmpty && ( 
        <p className="text-sm text-gray-400">{emptyMessage ?? 'No movies found.'}</p>
      )}
    </section>
  );
}
