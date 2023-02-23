/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        signtalk: {
          100: "#d8edeb",
          200: "#b1dbd7",
          300: "#8bcac2",
          400: "#64b8ae",
          500: "#3da69a",
          600: "#31857b",
          700: "#25645c",
          800: "#18423e",
          900: "#0c211f"
        },
      },
    },
  },
  plugins: [],
};