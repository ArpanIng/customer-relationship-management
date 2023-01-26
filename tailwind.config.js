/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/*.html',
    './accounts/templates/accounts/*.html',
    './clients/templates/clients/*.html',
    './dashboards/templates/dashboards/*.html',
    './leads/templates/leads/*.html',
    './teams/templates/teams/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
