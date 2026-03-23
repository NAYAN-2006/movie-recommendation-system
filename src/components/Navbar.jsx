import { Link, NavLink, useNavigate } from 'react-router-dom';
import useAuth from '../context/useAuth.js';

const navLinkClasses =
  'px-3 py-2 text-sm font-medium text-gray-300 hover:text-white hover:bg-zinc-800 rounded-md transition';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="fixed inset-x-0 top-0 z-30 bg-gradient-to-b from-black/80 via-black/40 to-transparent backdrop-blur">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex items-center justify-between h-16">
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2">
            <span className="h-7 w-7 rounded-sm bg-primary" />
            <span className="text-xl font-semibold tracking-tight">
              Movie<span className="text-primary">Sense</span>
            </span>
          </Link>
          <div className="hidden md:flex items-center gap-1">
            <NavLink to="/" className={navLinkClasses}>
              Home
            </NavLink>
            <NavLink to="/recommendations" className={navLinkClasses}>
              Recommendations
            </NavLink>
            {isAuthenticated && (
              <NavLink to="/profile" className={navLinkClasses}>
                Profile
              </NavLink>
            )}
          </div>
        </div>

        <div className="flex items-center gap-3">
          {!isAuthenticated ? (
            <>
              <Link to="/login" className="text-sm text-gray-300 hover:text-white">
                Login
              </Link>
              <Link
                to="/register"
                className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-red-700 transition"
              >
                Sign Up
              </Link>
            </>
          ) : (
            <>
              <span className="hidden sm:inline text-sm text-gray-300">
                {user?.name ?? 'Account'}
              </span>
              <button
                type="button"
                onClick={handleLogout}
                className="rounded-md border border-zinc-700 px-3 py-1.5 text-sm text-gray-200 hover:bg-zinc-800 transition"
              >
                Logout
              </button>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}

