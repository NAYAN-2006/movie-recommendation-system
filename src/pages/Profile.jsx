import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchUserProfile, fetchWatchHistory } from '../services/movieService.js';
import { useAuth } from '../context/AuthContext.jsx';
import MovieCard from '../components/MovieCard.jsx';

export default function Profile() {
  const { token, user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!token) return;
    const load = async () => {
      setLoading(true);
      setError('');
      try {
        const [{ data: profileData }, { data: historyData }] = await Promise.all([
          fetchUserProfile(),
          fetchWatchHistory(),
        ]);
        setProfile(profileData);
        setHistory(historyData.history ?? historyData);
      } catch {
        setError('Failed to load profile.');
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [token]);

  if (!token) {
    return (
      <div className="space-y-4">
        <div>
          <h1 className="text-3xl font-semibold text-white">Your Profile</h1>
          <p className="text-sm text-gray-400">
            Log in to view your account details, watch history, and rated movies.
          </p>
        </div>
        <div className="rounded-2xl bg-zinc-950/60 p-6 ring-1 ring-zinc-800">
          <p className="text-sm text-gray-300">You’re not logged in.</p>
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
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 rounded-2xl bg-zinc-950/60 p-6 ring-1 ring-zinc-800 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/80 text-lg font-semibold">
            {(profile?.name ?? user?.name ?? 'U').charAt(0).toUpperCase()}
          </div>
          <div>
            <h1 className="text-xl font-semibold text-white">
              {profile?.name ?? user?.name}
            </h1>
            <p className="text-sm text-gray-400">
              {profile?.email ?? user?.email}
            </p>
          </div>
        </div>
      </section>

      {loading && <p className="text-sm text-gray-400">Loading profile...</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}

      <section className="space-y-3">
        <h2 className="text-lg font-semibold text-white">Watch History</h2>
        {history.length === 0 ? (
          <p className="text-sm text-gray-400">No movies watched yet.</p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
            {history.map((item) => (
              <MovieCard key={item.id ?? item.movieId} movie={item} />
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

