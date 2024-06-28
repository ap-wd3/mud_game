/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}", 
    "./screens/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      flex: {
        '1.2': '1.2 1.2 0%',
      },
    },
      fontFamily: {
        'dangrek': ['Dangrek_400Regular'],
      },
  plugins: [],
}
}