import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
// eslint-disable-next-line no-unused-vars
import { motion } from 'framer-motion';
import { fetchRecommendations } from '../services/movieService.js';
import useAuth from '../context/useAuth.js';
import MovieCard from '../components/MovieCard.jsx';
import SkeletonMovieCard from '../components/SkeletonMovieCard.jsx';

const cardVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0 },
};

export default function Recommendations() {
  const { token, user } = useAuth();
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token || !user?.id) return;
    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const { data } = await fetchRecommendations(user.id);
        setMovies(data.movies ?? data);
      } catch {
        setError('Failed to load recommendations.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [token, user?.id]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-white">Recommended for You</h1>
        <p className="text-sm text-gray-400">
          Hand-picked titles based on your watch history and preferences.
        </p>
      </div>

      {!token && (
        <div className="rounded-2xl bg-zinc-950/60 p-6 ring-1 ring-zinc-800">
          <p className="text-sm text-gray-300">
            Please log in to see your personalized recommendations.
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link
              to="/login"
              className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 transition"
            >
              Go to Login
            </Link>
            <Link
              to="/register"
              className="rounded-lg border border-zinc-700 px-4 py-2 text-sm font-semibold text-gray-200 hover:bg-zinc-900 transition"
            >
              Create Account
            </Link>
          </div>
        </div>
      )}

      {error && <p className="text-sm text-red-400">{error}</p>}

      <section>
        <motion.div
          className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: { transition: { staggerChildren: 0.05 } },
          }}
        >
          {loading
            ? Array.from({ length: 10 }).map((_, idx) => (
                <motion.div
                  key={idx}
                  variants={cardVariants}
                  className="w-full"
                >
                  <SkeletonMovieCard />
                </motion.div>
              ))
            : movies.map((movie) => (
                <motion.div
                  key={movie.id ?? movie.movie_id}
                  variants={cardVariants}
                  className="w-full"
                >
                  <MovieCard movie={movie} />
                </motion.div>
              ))}
        </motion.div>
      </section>
    </div>
  );
}

