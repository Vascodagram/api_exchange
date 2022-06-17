# api_exchange

Запуск >> (sudo) docker-compose up

post http://localhost:8000/api/v1/price/

Получить все доступные валютные пары и их цену на биржах binance & kraken: { "symbol": "", "exchange": "", }

Получить все валютные пары указаной биржы: {
"symbol": "" "exhange": "kraken" or "binance" }

Получить конткретную валютную пару на заданной бирже: {
"symbol": "1INCHEUR" "exhange": "kraken" }
