import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import AuthProvider from './context/AuthContext.jsx';
import useAuth from './context/useAuth.js';
import Navbar from './components/Navbar.jsx';
import Home from './pages/Home.jsx';
import AuthPage from './pages/AuthPage.jsx';
import MovieDetails from './pages/MovieDetails.jsx';
import Recommendations from './pages/Recommendations.jsx';
import Profile from './pages/Profile.jsx';

function HomeGate() {
  const { token } = useAuth();
  if (!token) return <Navigate to="/login" replace />;
  return <Home />;
}

function AppContent() {
  const location = useLocation();
  const isAuthPage = ['/login', '/signup', '/register'].includes(location.pathname);

  return (
    <div className="min-h-screen bg-gradient-to-b from-black via-zinc-950 to-black text-gray-100">
      {!isAuthPage && <Navbar />}
      
      {isAuthPage ? (
        <Routes>
          <Route path="/login" element={<AuthPage mode="login" />} />
          <Route path="/signup" element={<AuthPage mode="signup" />} />
          <Route path="/register" element={<AuthPage mode="signup" />} />
        </Routes>
      ) : (
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-10">
          <Routes>
            <Route path="/" element={<HomeGate />} />
            <Route path="/movie/:id" element={<MovieDetails />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </main>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;

