import base64
from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT="""Tienes que analizar la imagen y considerar el prompt del usuario""".strip()

def image_prompt(user_prompt, encoded_image):
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": SYSTEM_PROMPT,
            },
            {
            "role": "user", 
            "content": user_prompt + encoded_image
            }
        ],
        max_tokens=40000,    
)
    print(response.choices[0])
    #print(response.usage)
    return response.choices[0].message.content

 
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

image_path = "../images/fine.webp"

MyEncodedImage = encode_image_to_base64(image_path)
print(f"Size in bytes of the image is : {MyEncodedImage.__sizeof__()/1024:2.2f}")
