import { useCallback, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchMovieDetails, rateMovie } from '../services/movieService.js';
import RatingStars from '../components/RatingStars.jsx';
import useAuth from '../context/useAuth.js';
import { getMoviePoster } from '../utils/movieHelpers.js';

export default function MovieDetails() {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [movie, setMovie] = useState(null);
  const [userRating, setUserRating] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const loadMovie = useCallback(async () => {
    setError('');
    try {
      const { data } = await fetchMovieDetails(id);
      setMovie(data);
      if (data.userRating) setUserRating(data.userRating);
    } catch {
      setError('Failed to load movie details.');
    }
  }, [id]);

  useEffect(() => {
    loadMovie();
  }, [loadMovie]);

  const handleRate = async (rating) => {
    if (!isAuthenticated) return;
    setSubmitting(true);
    try {
      await rateMovie(id, rating);
      setUserRating(rating);
      await loadMovie();
    } catch {
      setError('Failed to submit rating.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!movie && !error) {
    return <p className="text-sm text-gray-400">Loading movie...</p>;
  }

  if (error) {
    return <p className="text-sm text-red-400">{error}</p>;
  }

  return (
    <div className="grid gap-8 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]">
      <div className="space-y-4">
        <div className="overflow-hidden rounded-xl bg-zinc-900 ring-1 ring-white/10">
          {getMoviePoster(movie) ? (
            <img
              src={getMoviePoster(movie)}
              alt={movie?.title ?? 'Movie poster'}
              className="w-full object-cover"
              loading="lazy"
            />
          ) : (
            <div className="flex aspect-[2/3] w-full items-center justify-center bg-gradient-to-br from-zinc-900 via-black to-zinc-900 p-6">
              <div className="text-center">
                <div className="text-xs uppercase tracking-widest text-gray-400">
                  MovieSense
                </div>
                <div className="mt-2 text-lg font-semibold text-white">
                  {movie?.title ?? 'Untitled'}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="space-y-4">
        <h1 className="text-3xl font-bold text-white">{movie?.title}</h1>
        <div className="space-y-2">
          <h2 className="text-sm font-semibold text-white uppercase tracking-wide">
            Summary
          </h2>
          <p className="text-sm leading-relaxed text-gray-300">
            {movie?.longDescription ?? movie?.description}
          </p>
        </div>

        <div className="flex flex-wrap gap-3 text-sm text-gray-300">
          {movie?.genre && (
            <span className="rounded-full bg-zinc-900 px-3 py-1">
              {Array.isArray(movie.genre) ? movie.genre.join(' • ') : movie.genre}
            </span>
          )}
          {movie?.director && <span>Director: {movie.director}</span>}
          {movie?.actors && (
            <span>
              Cast:{' '}
              {Array.isArray(movie.actors) ? movie.actors.join(', ') : movie.actors}
            </span>
          )}
        </div>

        <div className="space-y-2">
          <p className="text-sm text-gray-300">
            Average rating:{' '}
            <span className="font-semibold text-accent">
              {movie?.rating?.toFixed ? movie.rating.toFixed(1) : movie?.rating ?? 'N/A'}
            </span>
          </p>
          <RatingStars value={movie?.rating ?? 0} readOnly size="lg" />
        </div>

        <div className="mt-4 space-y-2 border-t border-zinc-800 pt-4">
          <h2 className="text-sm font-semibold text-white uppercase tracking-wide">
            Your Rating
          </h2>
          {!isAuthenticated ? (
            <p className="text-xs text-gray-400">Login to rate this movie.</p>
          ) : (
            <div className="flex items-center gap-3">
              <RatingStars
                value={userRating}
                onChange={handleRate}
                size="lg"
                readOnly={submitting}
              />
              {submitting && (
                <span className="text-xs text-gray-400">Saving...</span>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

