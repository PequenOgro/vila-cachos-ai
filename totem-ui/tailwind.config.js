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
        brand: {
          50: '#fdf8f6',
          100: '#f2e8e5',
          200: '#eaddd7',
          500: '#b46d53',
          600: '#9d563d',
          700: '#7a3e2a',
          800: '#5c2d1e',
          900: '#3d1c13',
        },
        sage: {
          50: '#f4f7f4',
          100: '#e5ece5',
          500: '#628b64',
          600: '#4e7250',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
