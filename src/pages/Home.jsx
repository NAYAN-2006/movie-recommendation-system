import { useEffect, useMemo, useState } from 'react';
import useAuth from '../context/useAuth.js';
import { fetchMovies, fetchRecommendations } from '../services/movieService.js';
import HeroBanner from '../components/HeroBanner.jsx';
import MovieRow from '../components/MovieRow.jsx';
import SearchBar from '../components/SearchBar.jsx';
import { getMovieRating } from '../utils/movieHelpers.js';

export default function Home() {
  const { token, user } = useAuth();
  const [queryState, setQueryState] = useState({ query: '', genre: null });
  const [movies, setMovies] = useState([]);
  const [recommended, setRecommended] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loadingMovies, setLoadingMovies] = useState(false);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const [error, setError] = useState('');

  const loadMovies = async () => {
    setLoadingMovies(true);
    setError('');
    try {
      const { data } = await fetchMovies({
        search: queryState.query || undefined,
        genre: queryState.genre || undefined,
      });
      const fetched = data.movies ?? data;
      setMovies(fetched);
      if (data.genres) setGenres(data.genres);
    } catch {
      setError('Failed to load movies.');
    } finally {
      setLoadingMovies(false);
    }
  };

  const loadRecommendations = async () => {
    if (!token || !user?.id) return;
    setLoadingRecs(true);
    try {
      const { data } = await fetchRecommendations(user.id);
      setRecommended(data.movies ?? data);
    } catch {
      // Quietly fail; recommendations are optional
    } finally {
      setLoadingRecs(false);
    }
  };

  useEffect(() => {
    loadMovies();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryState.query, queryState.genre]);

  useEffect(() => {
    loadRecommendations();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token, user?.id]);

  const trending = useMemo(() => movies.slice(0, 12), [movies]);
  const topRated = useMemo(
    () =>
      [...movies]
        .sort((a, b) => getMovieRating(b) - getMovieRating(a))
        .slice(0, 12),
    [movies]
  );

  const recommendedMovies = useMemo(() => {
    if (token && recommended.length) return recommended;
    return movies.slice(0, 12);
  }, [movies, recommended, token]);

  const featuredMovie = useMemo(() => trending[0] || movies[0] || null, [trending, movies]);

  return (
    <div className="space-y-10">
      <HeroBanner movie={featuredMovie} />

      <div className="space-y-8">
        <div className="space-y-3">
          <h1 className="text-3xl font-semibold text-white">Browse</h1>
          <p className="text-sm text-gray-400">
            Discover trending picks, top rated hits, and personalized recommendations.
          </p>
          <SearchBar
            query={queryState.query}
            genre={queryState.genre}
            genres={genres}
            onChange={setQueryState}
          />
        </div>

        {error && <p className="text-sm text-red-400">{error}</p>}

        <MovieRow title="Trending Movies" movies={trending} loading={loadingMovies} />
        <MovieRow title="Top Rated" movies={topRated} loading={loadingMovies} />
        <MovieRow
          title="Recommended"
          movies={recommendedMovies}
          loading={loadingRecs || loadingMovies}
          emptyMessage={token ? 'No recommendations yet. Rate some movies to get personalized picks.' : 'Login to see personalized recommendations.'}
        />
      </div>
    </div>
  );
}

