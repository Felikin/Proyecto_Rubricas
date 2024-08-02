from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from prompts.prompts import *
import os
import pandas as pd


load_dotenv()

# Definición del modelo
llm = ChatOpenAI(
    model="gpt-4o-mini-2024-07-18",
    api_key=os.environ.get("OPENAI_API_KEY"),
    temperature=0
)

# Cargar transcripción de la clase
archivo = "Juan.txt"
with open(archivo, "r", encoding="utf-8") as file:
    transcripcion = file.read()

# Definición de la cadena de ejecución
chain_rubricas = prompt_rubricas | llm | output_parser

# Ejecución del prompt
results = chain_rubricas.invoke(input={"transcripcion": transcripcion})

# Visualización de resultados
print(results["rubricas"])