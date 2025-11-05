import requests
import time
import os

# === ⚙️ CONFIGURATION ===
TOKEN = os.getenv("") 
CHAT_ID = os.getenv("")

CRYPTO_IDS = ["bitcoin", "ethereum", "pepe", "shiba-inu"]
SEUIL_VARIATION = 5       # % de variation pour alerte
INTERVAL = 300            # 5 minutes

last_prices = {}


# === 💬 FONCTIONS TELEGRAM ===
def send_telegram_message(message: str):
    """Envoie un message sur Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"Erreur Telegram : {e}")


def get_telegram_updates(offset=None):
    """Récupère les messages/commandes envoyés au bot"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 10, "offset": offset}
    try:
        response = requests.get(url, params=params)
        return response.json().get("result", [])
    except Exception as e:
        print(f"Erreur lors de la récupération des updates : {e}")
        return []


# === 📊 FONCTIONS CRYPTO ===
def get_prices():
    """Récupère les prix des cryptos depuis CoinGecko"""
    ids = ",".join(CRYPTO_IDS)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    response = requests.get(url)
    return response.json()


def check_variations():
    """Vérifie les variations et envoie une alerte si nécessaire"""
    global last_prices
    prices = get_prices()
    messages = []

    for coin in CRYPTO_IDS:
        new_price = prices[coin]["usd"]
        old_price = last_prices.get(coin)

        if old_price:
            variation = ((new_price - old_price) / old_price) * 100
            if abs(variation) >= SEUIL_VARIATION:
                messages.append(f"💰 {coin.upper()} a bougé de {variation:.2f}% → {new_price}$")

        last_prices[coin] = new_price

    if messages:
        send_telegram_message("\n".join(messages))


def get_trending_coins():
    """Récupère les cryptos en tendance sur CoinGecko"""
    url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.get(url).json()
    coins = response.get("coins", [])
    return [coin["item"]["name"] for coin in coins]


# === 🧠 GESTION DES COMMANDES ===
def handle_command(text: str):
    """Analyse et exécute les commandes Telegram"""
    global SEUIL_VARIATION

    if text.startswith("/prix"):
        prices = get_prices()
        message = "📊 Prix actuels :\n"
        for coin in CRYPTO_IDS:
            message += f"{coin.upper()}: {prices[coin]['usd']} $\n"
        send_telegram_message(message)

    elif text.startswith("/seuil"):
        try:
            new_seuil = float(text.split(" ")[1])
            SEUIL_VARIATION = new_seuil
            send_telegram_message(f"⚙️ Seuil mis à jour : {SEUIL_VARIATION}%")
        except Exception:
            send_telegram_message("❌ Utilise `/seuil 5` pour définir un seuil")

    elif text.startswith("/tendance"):
        try:
            coins = get_trending_coins()
            message = "🔥 Cryptos en tendance :\n" + "\n".join(coins)
            send_telegram_message(message)
        except Exception as e:
            send_telegram_message(f"Erreur lors du scan des tendances : {e}")


# === 🔁 BOUCLE PRINCIPALE ===
if __name__ == "__main
