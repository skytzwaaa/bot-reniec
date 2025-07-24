import telebot
import requests
from config import BOT_TOKEN, API_RENIEC_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)

def consultar_dni(dni):
    url = f"https://dniruc.apisperu.com/api/v1/dni/{dni}?token={API_RENIEC_TOKEN}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("nombres"):
            return f"👤 *DNI:* {dni}\n*Nombre:* {data['nombres']} {data['apellidoPaterno']} {data['apellidoMaterno']}"
        else:
            return "⚠️ DNI no encontrado."
    else:
        return "❌ Error al consultar el DNI."

def buscar_por_nombre(nombre):
    # Simulación, ya que la API no lo permite por nombre
    return f"🔍 Buscaste: {nombre}\n⚠️ Actualmente solo está disponible la búsqueda por DNI."

@bot.message_handler(commands=["start"])
def enviar_bienvenida(mensaje):
    bot.reply_to(mensaje, "👋 ¡Hola! Envía un *DNI* o *nombre completo* para buscar datos.")

@bot.message_handler(func=lambda m: True)
def manejar_mensaje(mensaje):
    texto = mensaje.text.strip()

    if texto.isdigit() and len(texto) == 8:
        resultado = consultar_dni(texto)
    else:
        resultado = buscar_por_nombre(texto)

    bot.reply_to(mensaje, resultado, parse_mode="Markdown")

bot.polling()