/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#e50914',
        secondary: '#141414',
        accent: '#f5c518',
      },
      backgroundImage: {
        'gradient-overlay':
          'linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0.4), rgba(0,0,0,0.9))',
      },
    },
  },
  plugins: [],
};

