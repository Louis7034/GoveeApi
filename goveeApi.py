import requests
import time
from pynput import mouse
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

API_KEY = os.getenv("GOVEE_API_KEY")

if not API_KEY:
    raise ValueError("La clé API GOVEE_API_KEY est introuvable dans le fichier .env")

devices_salon = [
    {"device": "CB:D9:98:17:3C:6E:08:40", "model": "H6008", "name": "Lampadaire"},
    {"device": "22:4C:98:17:3C:6F:DB:2C", "model": "H6008", "name": "Salon canapé"},
    {"device": "6B:59:C5:39:32:33:58:85", "model": "H6066", "name": "Glide Hexa Pro Louis"},
    {"device": "42:C5:CA:35:34:37:2E:4B", "model": "H605C", "name": "RGBIC TV Backlight"},
    {"device": "8C:98:D0:C9:07:0E:67:70", "model": "H6008", "name": "Cuisine"},
    {"device": "64:FC:D0:C9:07:0C:20:F8", "model": "H6008", "name": "Smart LED Bulb Fado"}
]

headers = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

def send_command(device, model, cmd_name, cmd_value):
    """Envoie une commande à un appareil Govee."""
    payload = {
        "device": device,
        "model": model,
        "cmd": {"name": cmd_name, "value": cmd_value}
    }
    r = requests.put("https://developer-api.govee.com/v1/devices/control", headers=headers, json=payload)
    if r.status_code == 200:
        print(f"✅ {cmd_name}={cmd_value} → {device}")
    else:
        print(f"❌ Erreur avec {device}: {r.text}")

def allumer_salon():
    for dev in devices_salon:
        send_command(dev["device"], dev["model"], "turn", "on")
        time.sleep(0.5)

def eteindre_salon():
    for dev in devices_salon:
        send_command(dev["device"], dev["model"], "turn", "off")
        time.sleep(0.5)

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left:
            print("💡 Allumage du groupe 'Salon'...")
            allumer_salon()
        elif button == mouse.Button.right:
            print("💡 Extinction du groupe 'Salon'...")
            eteindre_salon()

if __name__ == "__main__":
    print("💡 Application en cours d'exécution. Cliquez gauche pour allumer, cliquez droit pour éteindre.")
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()