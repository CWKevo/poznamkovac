cd "$(dirname "$0")"

export FLASK_APP="poznamkovac.web:WEB"

(flask run --host 0.0.0.0 --port 5000 & uvicorn poznamkovac.web.api:API --host 0.0.0.0 --port 5001)

echo ""
read -p "Press [Enter] to continue..."
