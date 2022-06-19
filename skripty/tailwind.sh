cd "$(dirname "$0")/.."
cd tailwind

npx tailwindcss -i ../poznamkovac/web/staticke_subory/css/tailwind_zaklad.css -o ../poznamkovac/web/staticke_subory/css/produkcia.css
npx cleancss ../poznamkovac/web/staticke_subory/css/produkcia.css -o ../poznamkovac/web/staticke_subory/css/produkcia.min.css

rm ../poznamkovac/web/staticke_subory/css/produkcia.css
