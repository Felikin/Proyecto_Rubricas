from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import  JsonOutputParser
from src.prompts.object_models import Rubricas


# Prompt para bajas económicas 
output_parser = JsonOutputParser(pydantic_object=Rubricas)

format_instructions = output_parser.get_format_instructions()

prompt_rubricas = PromptTemplate(
    template="""
Eres una inteligencia artificial especializada en evaluar el desempeño de un docente en su clase a partir de la transcripción de la clase.
                                
Determina si el docente cumplió con cada una de las siguientes rúbricas:
- Nombre rúbrica: 3.       Da la bienvenida a los estudiantes y establece un tono de voz acorde para la sesión- Al igual saludar a través del Chat (inclusión). Descripción: "Evalúa si el docente da la bienvenida a los estudiantes al inicio de la clase y si utiliza un tono de voz apropiado, saludando también en el chat de manera inclusiva."
- Nombre rúbrica: 4.       Presenta el o los RA. Descripción: "¿Presentó el docente los Resultados de Aprendizaje (RA) al inicio de la clase, explicando su importancia y relevancia? Verifica si estos fueron mencionados y explicados en las diapositivas."
- Nombre rúbrica: 5.       Hace énfasis en el o los RA como declaración esperada al final por el estudiante. Descripción: "¿Enfatizó el docente los Resultados de Aprendizaje durante la clase? Evalúa si explicó que los RA son lo que se espera que los estudiantes logren al final de la asignatura."
- Nombre rúbrica: 6.       Usa Estrategias que lleven a enfatizar el o los RA. Descripción: "Evalúa si el docente utilizó estrategias adicionales (ejemplos prácticos, preguntas, actividades) para enfatizar los Resultados de Aprendizaje durante la clase."
- Nombre rúbrica: 7.       Las actividades tienen un proceso sistemático (Organización de la Sesión virtual). Descripción: "Revisa si las actividades en clase siguen una secuencia lógica y están organizadas de manera sistemática. Verifica si el docente presentó un esquema o agenda clara al inicio de la sesión."
- Nombre rúbrica: 8.       Presenta la agenda. Descripción: "¿Presentó el docente una agenda o esquema claro al inicio de la clase? Evalúa si esto ayudó a los estudiantes a entender la estructura de la sesión."
- Nombre rúbrica: 9.       Propicia el análisis con los estudiantes (Asegurarse de que las preguntas formuladas estén diseñadas para recordar, relacionar y comprender los conceptos relacionados con el o los RA.). Descripción: "Evalúa si el docente formuló preguntas que estimulan la curiosidad y el análisis crítico en los estudiantes, relacionadas con los conceptos presentados y los Resultados de Aprendizaje."
- Nombre rúbrica: 10.      Los invita a participar . Descripción: "¿Invitó el docente a los estudiantes a participar activamente durante la clase? Revisa si motivó a los estudiantes a compartir sus opiniones, responder preguntas o participar en discusiones."
- Nombre rúbrica: 11.      Lee las participaciones en el chat de los estudiantes y sobre este continua el desarrollo de su clase (retroalimentación). Descripción: "Evalúa si el docente utilizó las participaciones de los estudiantes en el chat para retroalimentar y enriquecer la clase. ¿Respondió a las preguntas o comentarios en tiempo real, integrando sus respuestas al desarrollo de la clase?"
- Nombre rúbrica: 12.      Alterna recursos en la clase. Descripción: "Revisa si el docente alternó el uso de diferentes recursos didácticos durante la clase, como diapositivas, videos, pizarra virtual, etc. Evalúa si la alternancia de estos recursos ayudó a mejorar la comprensión de los estudiantes."
- Nombre rúbrica: 15.      Sintetiza los puntos clave a partir de los RA de la clase. Descripción: "¿Hizo el docente una síntesis de los puntos clave de la clase al final, relacionándolos con los Resultados de Aprendizaje (RA)? Verifica si esta síntesis ayudó a los estudiantes a reforzar su comprensión."
- Nombre rúbrica: 16.      Invita a revisar la agenda semanal y realizar las lecturas y material complementario. Descripción: "Evalúa si al finalizar la sesión, el docente invitó a los estudiantes a revisar la agenda semanal y el material complementario disponible en la plataforma. ¿Se proporcionaron recomendaciones claras para la próxima sesión?"
- Nombre rúbrica: 17.      Invita al desarrollo de las actividades futuras. Descripción: "Revisa si el docente motivó a los estudiantes a trabajar en las actividades futuras, proporcionando orientaciones o recomendaciones para prepararse adecuadamente para las próximas sesiones."
- Nombre rúbrica: 18.      Despide la sesión. Descripción: "¿Realizó el docente una despedida adecuada al finalizar la clase, cerrando la sesión de manera profesional y amigable? Evalúa si el cierre fue claro y permitió a los estudiantes entender que la sesión había terminado."

Para cada una de las rúbricas debes crear un JSON con cuartro llaves:
- "Rúbrica": <Nombre de la rúbrica evaluada>.
- "Cumple": <Cumple o No cumple dependiendo de si el docente cumple con la rúbrica>.
- "Observación": <Razón por la que crees que el docente cumple o no con la rúbrica>.


transcrpición: 
{transcripcion}
                                 
{format_instructions}                                                              
""", input_variables=["transcripcion"], 
    partial_variables={"format_instructions": format_instructions})