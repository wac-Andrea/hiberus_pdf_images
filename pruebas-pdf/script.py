from openai import OpenAI
import openai
import pdfplumber
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],
)
def extract_text_from_pdf(pdf_path, **kwargs):
    """
    Function to extract text from a PDF and return it as plain text.

    Parameters:
    - pdf_path: str, path to the input PDF file (required)
    - **kwargs: additional optional arguments for pdfplumber's extract_text method, such as:
        - layout: bool, whether to preserve the layout (default: True)
        - line_dir_render: str, direction of line rendering (default: 'ttb')
        - char_dir_render: str, direction of character rendering (default: 'ltr')
        - x_tolerance: int, horizontal tolerance for grouping elements (default: 1)
        - y_tolerance: int, vertical tolerance for grouping elements (default: 1)

    Returns:
    - text: str, the extracted text from the PDF.
    """

    options = {
        "layout": True,
        "line_dir_render": "ttb",
        "char_dir_render": "ltr",
        "x_tolerance": 1,
        "y_tolerance": 1,
    }

    options.update(kwargs)

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text(
                layout=options["layout"],
                line_dir_render=options["line_dir_render"],
                char_dir_render=options["char_dir_render"],
                x_tolerance=options["x_tolerance"],
                y_tolerance=options["y_tolerance"],
            )
            text += "\n"

    return text

def pdf_text_prompt(client, extracted_text, user_text):

  SYSTEM_PROMPT = """Eres un ávido lector que es capaz de procesar rápidamente un texto
  y entender lo que pone. Te fijas en los detalles y contexto del texto. Además, tienes conocimientos en medicina y veterinaria
  por lo que se te hace muy fácil analizar un documento (por ejemplo, un informe)
  y saber qué le pasa al paciente. Sé claro y acertado en tus diagnósticos y respuestas. """

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
              "text": extracted_text
            },
            {
              "type": "text",
              "text": user_text
            }
          ]
        }
      ],
      max_completion_tokens= 16384,
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



pdf_path = "../pdfs/informe.pdf"  
extracted_text = extract_text_from_pdf(pdf_path)
user_text= "¿Qué le ocurre a la paciente?"

api_message_content=pdf_text_prompt(client,extracted_text, user_text)
print(api_message_content)