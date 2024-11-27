from openai import OpenAI
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "../images/pierna.webp"

base64_image = encode_image(image_path)

SYSTEM_PROMPT = """Eres una persona detallista y observadora. 
Cuando ves una imagen, te fijas en todos los detalles que contiene y sabes describirla a la perfección para
que otras personas entiendan lo que estás viendo. Además, tienes conocimientos en medicina y veterinaria
por lo que se te hace muy fácil analizar una imagen (por ejemplo, una radiografía o la foto de una herida)
y saber qué le pasa al paciente. Sé claro y acertado en tus diagnósticos y respuestas."""

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Este paciente se queja de dolores de cabeza. ¿Te da la radiografía una pista de qué le ocurre?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 3000
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json()['choices'][0]['message']['content'])