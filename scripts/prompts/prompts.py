from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser, JsonOutputParser
from langchain_core.output_parsers.list import NumberedListOutputParser
from prompts.object_models import Rubrica, Rubricas


# Prompt para bajas económicas 
output_parser = JsonOutputParser(pydantic_object=Rubricas)

format_instructions = output_parser.get_format_instructions()

prompt_rubricas = PromptTemplate(
    template="""
Eres una inteligencia artificial especializada en evaluar el desempeño de un docente en su clase a partir de la transcripción de la clase.
                                
Determina si el docente cumplió con cada una de las siguientes rúbricas:
- Dar la bienvenida a la clase.
- Presentó los resultados de aprendizaje.
- Presenta la agenda de la clase.
- Expone los resultados de aprendizaje, es decir, los explica detalladamente.
- Propone preguntas para que los estudiantes comprendan los contenidos.
- Invita a participar a los estudiantes.
- Lee los aportes de los estudiantes en el chat de la clase.
- Al final de la clase sintentiza los puntos claves a partir de los resultados de aprendizaje.
- Invita a revisar la agenda semanal y realizar las lecturas y material complementario.
- Invita al desarrollo de actividades futuras.
- Se despide de sus estudiantes al final de la clase.
                            
Para cada una de las rúbricas debes crear un JSON con cuartro llaves:
- "Rúbrica": <Nombre de la rúbrica evaluada>.
- "Cumple": <Sí o No dependiendo de si el docente cumple con la rúbrica>.
- "Justificación": <Razón por la que crees que el docente cumple con la rúbrica>.
- "Fragmento": <Fragmento de la clase que sustente tu respuesta>.


transcrpición: 
{transcripcion}
                                 
{format_instructions}                                                              
""", input_variables=["transcripcion"], 
    partial_variables={"format_instructions": format_instructions})
