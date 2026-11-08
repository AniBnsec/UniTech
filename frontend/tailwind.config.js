/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          950: '#070b14',
          900: '#0b1329',
          800: '#111d40',
          700: '#1b2b5a',
          blue: '#00f0ff',
          emerald: '#00ffaa',
          amber: '#ffb700',
          rose: '#ff0055',
          purple: '#9d4edd'
        }
      }
    },
  },
  plugins: [],
}

