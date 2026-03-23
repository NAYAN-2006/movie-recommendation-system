import { useLocation } from 'react-router-dom';
import AuthForm from '../components/AuthForm.jsx';
import VideoBackground from '../components/VideoBackground.jsx';

export default function AuthPage({ mode }) {
  const location = useLocation();
  const isLogin = mode === 'login';

  return (
    <div className="relative min-h-screen overflow-hidden">
      <VideoBackground src="/background.mp4" />

      <div className="relative z-10 flex min-h-screen items-center justify-center px-4 py-10">
        <div className="absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-black/70 to-transparent" />

        <div className="w-full max-w-5xl">
          <div className="grid gap-10 lg:grid-cols-2 lg:items-center">
            <div className="hidden lg:block">
              <div className="max-w-md">
                <p className="text-sm font-semibold tracking-wider text-primary">
                  MOVIESENSE
                </p>
                <h2 className="mt-3 text-4xl font-semibold leading-tight text-white">
                  {isLogin ? 'Pick up where you left off.' : 'Start your next favorite story.'}
                </h2>
                <p className="mt-4 text-sm text-gray-300">
                  Personalized recommendations, watch history, and ratings—all in one place.
                </p>
                <div className="mt-6 space-y-3 text-sm text-gray-300">
                  <div className="flex items-center gap-3">
                    <span className="h-2 w-2 rounded-full bg-accent" />
                    <span>Discover movies by genre and cast.</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="h-2 w-2 rounded-full bg-accent" />
                    <span>Rate movies to improve recommendations.</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="h-2 w-2 rounded-full bg-accent" />
                    <span>Track your watch history.</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex justify-center lg:justify-end">
              <AuthForm mode={mode} key={location.pathname} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

