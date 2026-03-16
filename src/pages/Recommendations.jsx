import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchRecommendations } from '../services/movieService.js';
import { useAuth } from '../context/AuthContext.jsx';
import MovieCard from '../components/MovieCard.jsx';

export default function Recommendations() {
  const { token } = useAuth();
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) return;
    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const { data } = await fetchRecommendations();
        setMovies(data.movies ?? data);
      } catch {
        setError('Failed to load recommendations.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [token]);

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-3xl font-semibold text-white">For You</h1>
        <p className="text-sm text-gray-400">
          Movies recommended based on your taste and watch history.
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

      {loading && <p className="text-sm text-gray-400">Loading recommendations...</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}
      <section>
        <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      </section>
    </div>
  );
}

