import { useEffect, useState } from 'react';
import { fetchMovies } from '../services/movieService.js';
import MovieCard from '../components/MovieCard.jsx';
import SearchBar from '../components/SearchBar.jsx';

export default function Home() {
  const [queryState, setQueryState] = useState({ query: '', genre: null });
  const [movies, setMovies] = useState([]);
  const [genres, setGenres] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadMovies = async () => {
    setLoading(true);
    setError('');
    try {
      const { data } = await fetchMovies({
        search: queryState.query || undefined,
        genre: queryState.genre || undefined,
      });
      setMovies(data.movies ?? data);
      if (data.genres) setGenres(data.genres);
    } catch {
      setError('Failed to load movies.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMovies();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [queryState.query, queryState.genre]);

  return (
    <div className="space-y-6">
      <div className="space-y-3">
        <h1 className="text-3xl font-semibold text-white">Discover Movies</h1>
        <p className="text-sm text-gray-400">
          Search, filter by genre, and explore personalized recommendations.
        </p>
        <SearchBar
          query={queryState.query}
          genre={queryState.genre}
          genres={genres}
          onChange={setQueryState}
        />
      </div>

      {loading && <p className="text-sm text-gray-400">Loading movies...</p>}
      {error && <p className="text-sm text-red-400">{error}</p>}

      <section className="mt-2">
        <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      </section>
    </div>
  );
}

