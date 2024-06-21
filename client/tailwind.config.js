/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "../gacha_famg/templates/**/*.html",
    "./src/**/*.{js,ts,vue}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["retro"]
  }
}