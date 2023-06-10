import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('API_KEY')

import json

examples = json.load(open('data/examples.json'))['data']

qa_text = ""
for example in examples:
  if example['train']:
    qa_text += f"Q: {str(example['query'])}\n"
    qa_text += f"A: {json.dumps(example['answer'])}"
    qa_text += '\n'

prompt = lambda text: f"""
Te pasaré una consulta entre los simbolos <>. Tu tarea es:
1.- Reconocer si el texto es una consulta relacionada a desastres climaticos o centros asistenciales. Si ni lo es responder "null".
2.- Parsear la consulta y retornarn SOLO un JSON con los siguientes datos:
- ubicacion: string | null
- tipo_de_desastre: (incendio, tsunami, terremoto)
- centro_asistencial: (bomberos, policia, hospital, areas_verdes)
La respuesta deberá se, o null si no es relacionada, o el json.

Algunos ejemplos de QA:
{qa_text}
<{text}>
"""

prompt_disasters = lambda disasters, location: f"""
Te pasare una lista de desastres naturales en ingles en {location}.

- Primero explica que en la zona existen los desastres.
- Luego retorna un mensaje en español en no mas de 100 palabras para prevenir los desastres

Desastres: {disasters}
"""

prompt_disasters_and_hospitales = lambda disasters, location, ratio: f"""
Te pasare una lista de desastres naturales en ingles en {location}, Junto con la cantidad de hospitales
y el ratio desastre natural/centros asistenciales.

Un ratio cercano a 0 indica que hay que instalar mas centros asistenciales.
Un ratio cercano a 0.25 indica que no se esta tan mal, pero se puede mejorar.
Un ratio mayor a 0.5 indica que la zona esta bien.

- Primero explica que en la zona existen los desastres mencionados.
- Luego retorna un mensaje indicando si hay que instalar mas centros asistenciales o no, y por que. relacionandolo
con los desastres naturales.
- Luego retorna un mensaje en español en no mas de 100 palabras para prevenir los desastres

Desastres: {disasters}
Ratio desastre natural / centros asistenciales: {ratio}
"""

def _get_completion_gpt3_5(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

def parse_data(text):
  return json.loads(_get_completion_gpt3_5(prompt(text)))

def get_insights_of_disasters(disasters, location):
  return _get_completion_gpt3_5(prompt_disasters(disasters, location))

def get_insights_of_disasters_and_hospitals(disasters, location, ratio):
  return _get_completion_gpt3_5(prompt_disasters_and_hospitales(disasters, location, ratio))
