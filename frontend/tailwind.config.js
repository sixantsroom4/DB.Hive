/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#10a37f',
          hover: '#1a7f64',
        },
        surface: {
          DEFAULT: '#ffffff',
          secondary: '#f7f7f8',
        },
        border: {
          DEFAULT: '#e5e5e5',
          dark: '#d1d5db',
        },
      },
    },
  },
  plugins: [],
}
