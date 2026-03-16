import api from './api';

export const fetchMovies = (params) =>
  api.get('/movies', { params });

export const fetchMovieDetails = (id) =>
  api.get(`/movies/${id}`);

export const rateMovie = (id, rating) =>
  api.post(`/movies/${id}/rate`, { rating });

export const fetchRecommendations = () =>
  api.get('/recommendations');

export const fetchUserProfile = () =>
  api.get('/users/profile');

export const fetchWatchHistory = () =>
  api.get('/users/watch-history');

