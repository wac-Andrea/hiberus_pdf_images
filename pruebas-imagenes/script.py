from openai import OpenAI
import openai
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def image_text_prompt(client,base64_image, user_text):
  SYSTEM_PROMPT = """Eres una persona detallista y observadora. 
  Cuando ves una imagen, te fijas en todos los detalles que contiene y sabes describirla a la perfección para
  que otras personas entiendan lo que estás viendo. Además, tienes conocimientos en medicina y veterinaria
  por lo que se te hace muy fácil analizar una imagen (por ejemplo, una radiografía o la foto de una herida)
  y saber qué le pasa al paciente. Sé claro y acertado en tus diagnósticos y respuestas."""

  try:
    response = client.chat.completions.create(
    model = "gpt-4o",
    messages = [
        {
          "role": "system",
          "content": SYSTEM_PROMPT
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": user_text
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
      max_completion_tokens = 16384,
    ) 
  
    return response.choices[0].message.content

  except openai.BadRequestError as e:
      print(f"La petición no se ha completado con éxito: {e}")
      exit(1)  

  except openai.AuthenticationError:
      print("Error: El formato no es correcto. Error en las claves (keys)")
      exit(1)  

  except Exception as e:
      print(f"Ha ocurrido un error inesperado: {e}")
      exit(1)  



image_path = "../images/informe.jpg"
base64_image = encode_image(image_path)
user_text= "Este paciente se queja de dolores de cabeza. ¿Te da la radiografía una pista de qué le ocurre?"

api_message_content = image_text_prompt(client, base64_image, user_text)
print(api_message_content)