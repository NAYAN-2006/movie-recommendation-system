// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

function getBackgroundImage(movie) {
  if (!movie) return null;
  return movie.backdropUrl || movie.posterUrl || movie.imageUrl || null;
}

export default function HeroBanner({ movie, onPlay, onMoreInfo }) {
  const navigate = useNavigate();
  const bg = getBackgroundImage(movie);

  const handlePlay = () => {
    if (onPlay) return onPlay(movie);
    if (movie?.id) navigate(`/movie/${movie.id}`);
  };

  const handleMoreInfo = () => {
    if (onMoreInfo) return onMoreInfo(movie);
    if (movie?.id) navigate(`/movie/${movie.id}`);
  };

  const title = movie?.title ?? 'Featured Movie';
  const overview = movie?.description || movie?.overview || movie?.tagline || '';

  return (
    <section className="relative isolate overflow-hidden rounded-3xl bg-black/30">
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: bg
            ? `linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.2)), url('${bg}')`
            : 'linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.2))',
        }}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
      <div className="relative mx-auto flex max-w-7xl flex-col gap-6 px-6 py-16 md:px-12 lg:px-16">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
          className="max-w-2xl"
        >
          <h1 className="text-3xl font-semibold tracking-tight text-white sm:text-5xl md:text-6xl">
            {title}
          </h1>
          {overview ? (
            <p className="mt-4 max-w-xl text-sm text-gray-200/90 sm:text-base">
              {overview.length > 220 ? `${overview.slice(0, 220).trim()}…` : overview}
            </p>
          ) : (
            <p className="mt-4 max-w-xl text-sm text-gray-200/70 sm:text-base">
              Discover, stream, and enjoy a curated selection just for you.
            </p>
          )}
          <div className="mt-6 flex flex-wrap items-center gap-3">
            <motion.button
              type="button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              className="inline-flex items-center justify-center gap-2 rounded-full bg-primary px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-red-500/40 transition focus:outline-none focus:ring-2 focus:ring-primary/70"
              onClick={handlePlay}
            >
              ▶ Play
            </motion.button>
            <motion.button
              type="button"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.98 }}
              className="inline-flex items-center justify-center gap-2 rounded-full border border-white/20 bg-white/10 px-6 py-3 text-sm font-semibold text-white backdrop-blur transition focus:outline-none focus:ring-2 focus:ring-white/30"
              onClick={handleMoreInfo}
            >
              ℹ More Info
            </motion.button>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
