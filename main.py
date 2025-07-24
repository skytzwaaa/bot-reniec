import telebot
import requests
import json

# Reemplaza con tu propio token del Bot de Telegram
BOT_TOKEN = "TU_TOKEN_AQUI"

# Crea una instancia del bot
bot = telebot.TeleBot(BOT_TOKEN)

# Función para consultar por DNI
def consultar_dni(dni):
    url = f"https://dniruc.apisperu.com/api/v1/dni/{dni}?token=TU_API_TOKEN_AQUI"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("nombres"):
            return f"👤 *DNI:* {dni}\n*Nombre:* {data['nombres']} {data['apellidoPaterno']} {data['apellidoMaterno']}"
        else:
            return "⚠️ DNI no encontrado."
    else:
        return "❌ Error al consultar el DNI."

# Comando /start
@bot.message_handler(commands=["start"])
def enviar_bienvenida(mensaje):
    bot.reply_to(mensaje, "👋 ¡Hola! Envía un DNI para buscar datos.")

# Cuando el usuario envía un mensaje (DNI)
@bot.message_handler(func=lambda m: True)
def manejar_mensaje(mensaje):
    dni = mensaje.text.strip()
    if dni.isdigit() and len(dni) == 8:
        resultado = consultar_dni(dni)
        bot.reply_to(mensaje, resultado, parse_mode="Markdown")
    else:
        bot.reply_to(mensaje, " Por favor, envía un número de DNI válido (8 dígitos).")

# Inicia el bot
bot.polling()
