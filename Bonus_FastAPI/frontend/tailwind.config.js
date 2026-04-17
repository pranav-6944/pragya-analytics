/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
      colors: {
        navy: { 900: '#0F172A', 800: '#1E293B', 700: '#334155', 600: '#475569' },
        accent: { DEFAULT: '#6366F1', light: '#EEF2FF', hover: '#4F46E5', glow: 'rgba(99,102,241,0.12)' },
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease forwards',
        'fade-in': 'fadeIn 0.4s ease forwards',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        fadeUp: { '0%': { opacity:0, transform:'translateY(24px)' }, '100%': { opacity:1, transform:'translateY(0)' } },
        fadeIn: { '0%': { opacity:0 }, '100%': { opacity:1 } },
        float: { '0%,100%': { transform:'translateY(0)' }, '50%': { transform:'translateY(-8px)' } },
      }
    },
  },
  plugins: [],
}
