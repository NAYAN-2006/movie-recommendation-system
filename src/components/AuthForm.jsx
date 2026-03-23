import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import useAuth from '../context/useAuth.js';

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).toLowerCase());
}

export default function AuthForm({ mode }) {
  const isLogin = mode === 'login';
  const navigate = useNavigate();
  const location = useLocation();
  const { login, register, loading, token } = useAuth();

  const [values, setValues] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');

  const nextPath = location.state?.from?.pathname || '/';

  useEffect(() => {
    if (!isLogin) return;
    if (!token) return;
    navigate(nextPath, { replace: true });
  }, [isLogin, token, navigate, nextPath]);

  const canSubmit = useMemo(() => {
    if (!validateEmail(values.email)) return false;
    if (!values.password || values.password.length < 6) return false;
    if (!isLogin) {
      if (!values.name.trim()) return false;
      if (values.password !== values.confirmPassword) return false;
    }
    return true;
  }, [isLogin, values]);

  const onChange = (e) => {
    setValues((v) => ({ ...v, [e.target.name]: e.target.value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!canSubmit) {
      setError('Please check your inputs and try again.');
      return;
    }

    try {
      if (isLogin) {
        await login({ email: values.email, password: values.password });
        navigate(nextPath, { replace: true });
      } else {
        await register({ name: values.name, email: values.email, password: values.password });
        navigate('/login', { replace: true });
      }
    } catch (err) {
      const msg =
        err?.response?.data?.message ||
        err?.message ||
        'Request failed. Please try again.';
      setError(msg);
    }
  };

  return (
    <div className="w-full max-w-md">
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-semibold tracking-tight text-white">
          {isLogin ? 'Welcome back' : 'Create your account'}
        </h1>
        <p className="mt-2 text-sm text-gray-300">
          {isLogin
            ? 'Sign in to get personalized movie recommendations.'
            : 'Join and start building your watch profile.'}
        </p>
      </div>

      <div className="rounded-2xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-black/60 backdrop-blur-xl">
        {error && (
          <div className="mb-4 rounded-lg border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-200">
            {error}
          </div>
        )}

        <form onSubmit={onSubmit} className="space-y-4">
          {!isLogin && (
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-gray-200" htmlFor="name">
                Name
              </label>
              <input
                id="name"
                name="name"
                value={values.name}
                onChange={onChange}
                className="w-full rounded-xl bg-black/40 px-4 py-2.5 text-sm text-white ring-1 ring-white/10 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Your name"
                autoComplete="name"
                required
              />
            </div>
          )}

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-gray-200" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={values.email}
              onChange={onChange}
              className="w-full rounded-xl bg-black/40 px-4 py-2.5 text-sm text-white ring-1 ring-white/10 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="you@example.com"
              autoComplete="email"
              required
            />
            {values.email && !validateEmail(values.email) && (
              <p className="text-xs text-amber-200/90">Enter a valid email address.</p>
            )}
          </div>

          <div className="space-y-1.5">
            <label className="text-sm font-medium text-gray-200" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={values.password}
              onChange={onChange}
              className="w-full rounded-xl bg-black/40 px-4 py-2.5 text-sm text-white ring-1 ring-white/10 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="••••••••"
              autoComplete={isLogin ? 'current-password' : 'new-password'}
              required
            />
            {values.password && values.password.length < 6 && (
              <p className="text-xs text-amber-200/90">Use at least 6 characters.</p>
            )}
          </div>

          {!isLogin && (
            <div className="space-y-1.5">
              <label className="text-sm font-medium text-gray-200" htmlFor="confirmPassword">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                value={values.confirmPassword}
                onChange={onChange}
                className="w-full rounded-xl bg-black/40 px-4 py-2.5 text-sm text-white ring-1 ring-white/10 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="••••••••"
                autoComplete="new-password"
                required
              />
              {values.confirmPassword && values.password !== values.confirmPassword && (
                <p className="text-xs text-amber-200/90">Passwords do not match.</p>
              )}
            </div>
          )}

          <button
            type="submit"
            disabled={!canSubmit || loading}
            className="group relative w-full overflow-hidden rounded-xl bg-primary px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-primary/20 transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <span className="relative z-10">
              {loading ? (isLogin ? 'Signing in…' : 'Creating account…') : isLogin ? 'Login' : 'Sign Up'}
            </span>
            <span className="absolute inset-0 -translate-x-full bg-white/20 transition-transform duration-500 group-hover:translate-x-0" />
          </button>
        </form>

        <div className="mt-5 flex items-center justify-between gap-3 text-xs text-gray-300">
          <span className="h-px flex-1 bg-white/10" />
          <span>or</span>
          <span className="h-px flex-1 bg-white/10" />
        </div>

        <p className="mt-4 text-center text-sm text-gray-300">
          {isLogin ? (
            <>
              Don’t have an account?{' '}
              <Link to="/signup" className="font-semibold text-accent hover:underline">
                Sign up
              </Link>
            </>
          ) : (
            <>
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-accent hover:underline">
                Log in
              </Link>
            </>
          )}
        </p>
      </div>
    </div>
  );
}

