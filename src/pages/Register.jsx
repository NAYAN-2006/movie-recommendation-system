import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

export default function Register() {
  const { register, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');

  const handleChange = (e) =>
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    try {
      await register({
        name: form.name,
        email: form.email,
        password: form.password,
      });
      navigate('/login');
    } catch {
      setError('Failed to create account.');
    }
  };

  return (
    <div className="mx-auto max-w-md space-y-6">
      <div>
        <h1 className="text-3xl font-semibold text-white">Create your account</h1>
        <p className="text-sm text-gray-400">
          Join to get personalized movie recommendations.
        </p>
      </div>
      <form
        onSubmit={handleSubmit}
        className="space-y-4 rounded-2xl bg-zinc-950/60 p-6 ring-1 ring-zinc-800"
      >
        {error && <p className="text-sm text-red-400">{error}</p>}
        <div className="space-y-1.5">
          <label className="text-sm text-gray-200" htmlFor="name">
            Name
          </label>
          <input
            id="name"
            name="name"
            required
            className="w-full rounded-lg bg-zinc-900 px-3 py-2 text-sm text-gray-100 ring-1 ring-zinc-800 focus:outline-none focus:ring-2 focus:ring-primary"
            value={form.name}
            onChange={handleChange}
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-sm text-gray-200" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            className="w-full rounded-lg bg-zinc-900 px-3 py-2 text-sm text-gray-100 ring-1 ring-zinc-800 focus:outline-none focus:ring-2 focus:ring-primary"
            value={form.email}
            onChange={handleChange}
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-sm text-gray-200" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            required
            className="w-full rounded-lg bg-zinc-900 px-3 py-2 text-sm text-gray-100 ring-1 ring-zinc-800 focus:outline-none focus:ring-2 focus:ring-primary"
            value={form.password}
            onChange={handleChange}
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-sm text-gray-200" htmlFor="confirmPassword">
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            name="confirmPassword"
            type="password"
            required
            className="w-full rounded-lg bg-zinc-900 px-3 py-2 text-sm text-gray-100 ring-1 ring-zinc-800 focus:outline-none focus:ring-2 focus:ring-primary"
            value={form.confirmPassword}
            onChange={handleChange}
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="mt-2 w-full rounded-lg bg-primary py-2 text-sm font-semibold text-white hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? 'Creating account...' : 'Sign Up'}
        </button>
        <p className="text-xs text-gray-400">
          Already have an account?{' '}
          <Link to="/login" className="text-accent hover:underline">
            Sign in
          </Link>
        </p>
      </form>
    </div>
  );
}

