import os
from langchain_openai import ChatOpenAI
from src.prompts.prompts import *
from typing import List
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")

def model_execution(transcripcion: str) -> List[dict]:
    """
    Recibe una transcrición y devuelve la evaluación de las rúbricas.
    
    Args:
        transcripcion (str): Transcripción de un audio, usualmente una clase.
    Returns:
        List: Lista de diccionarios con la evaluación de las rúbricas.
    """
    
    llm = ChatOpenAI(
        model="gpt-4o-mini-2024-07-18",
        api_key=openai_api_key, # type:ignore
        temperature=0
    )
    chain_rubricas = prompt_rubricas | llm | output_parser
    results = chain_rubricas.invoke(input={"transcripcion": transcripcion})

    return results["rubricas"]