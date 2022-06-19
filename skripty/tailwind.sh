cd "$(dirname "$0")/.."
cd tailwind

npx tailwindcss -i ../poznamkovac/web/static/css/tailwind_zaklad.css -o ../poznamkovac/web/static/css/produkcia.css
npx cleancss ../poznamkovac/web/static/css/produkcia.css -o ../poznamkovac/web/static/css/produkcia.min.css

rm ../poznamkovac/web/static/css/produkcia.css
