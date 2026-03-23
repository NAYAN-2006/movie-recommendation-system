export function getMovieRating(movie) {
  if (!movie) return 0;
  if (typeof movie.rating === 'number') return movie.rating;
  if (typeof movie.average_rating === 'number') return movie.average_rating;
  const id = movie.id ?? movie.movie_id;
  if (typeof id === 'number') {
    // deterministic pseudo-rating based on id
    return Math.min(5, Math.max(0, ((id % 5) + 3) / 1.2));
  }
  return 3.5;
}

export function getMoviePoster(movie) {
  if (!movie) return null;
  return (
    movie.poster_url ||
    movie.backdrop_url ||
    movie.posterUrl ||
    movie.backdropUrl ||
    movie.imageUrl ||
    `https://picsum.photos/seed/${encodeURIComponent(movie.title || movie.id || 'movie')}/500/750`
  );
}

export function getMovieSubtitle(movie) {
  return movie?.description || movie?.overview || movie?.tagline || '';
}
