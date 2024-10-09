/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./frontend/src/templates/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}

// npx tailwindcss -i ./frontend/src/static/css/input.css -o ./frontend/src/static/css/output.css --watch