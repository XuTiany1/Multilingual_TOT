USER_CHAT_TEMPLATE = "<start_of_turn>usuario\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>modelo\n"

# standard prompt
standard_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Responde a la siguiente pregunta matemática. Introduce solo la respuesta final como un número y nada más.\n"
) + "{question}\nRespuesta: " + MODEL_CHAT_TEMPLATE

# cot prompt
cot_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Responde a la siguiente pregunta matemática. "
           "Piensa paso a paso y deja tu proceso de razonamiento a continuación. "
           "La última línea debe tener el formato 'La respuesta es xxx', donde xxx es un número.\n"
) + "Pregunta: {question}\nRespuesta paso a paso:\n" + MODEL_CHAT_TEMPLATE

# propose_prompt
propose_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Imagina que estás compuesto por {n} matemáticos independientes que hablan {lang}, "
           "cada uno con una perspectiva única sobre cómo abordar un problema matemático de varios pasos.\n\n"
           "Antes de responder con tu razonamiento, cada matemático debe comenzar su respuesta con "
           "'Matemático i: ', donde 'i' puede ser 1, 2 o 3.\n\n"
           "Basándose en la pregunta dada y el razonamiento actual, cada matemático generará de manera independiente "
           "un siguiente paso único, creativo y válido para resolver el problema. "
           "Cada paso debe diferir en el enfoque, utilizando diferentes métodos matemáticos, "
           "desgloses del problema o representaciones alternativas.\n\n"
           "Cada matemático explicará claramente y de manera concisa su razonamiento antes de proponer su siguiente paso. "
           "Solo agregarán su primer paso, permitiendo discusión y refinamiento posteriores.\n\n"
           "Si no hay contexto previo, esto marca el inicio del razonamiento, y los matemáticos propondrán "
           "diferentes formas de comenzar a resolver el problema.\n\n"
           "Este proceso continúa paso a paso hasta que se alcance una respuesta definitiva.\n\n"
) + "---\n" \
    "Pregunta: {question}\n\n" \
    "Contexto (razonamiento previo, si lo hay):\n{current_thought_process}\n\n" \
    "Lista de posibles pasos futuros (cada línea representa la perspectiva de un solo matemático):\n" \
    + MODEL_CHAT_TEMPLATE

# value_prompt
value_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Evalúa si el paso de razonamiento dado contribuye significativamente a resolver el problema. "
           "Responde solo con 'Evaluación: seguro', 'Evaluación: probable' o 'Evaluación: imposible'. "
           "No incluyas explicaciones ni ningún otro texto adicional.\n\n"
           "Asigna uno de los siguientes juicios:\n"
           "- seguro: El paso es correcto y representa un progreso lógico hacia la solución.\n"
           "- probable: El paso es plausible, pero puede necesitar refinamiento o carecer de detalles clave.\n"
           "- imposible: El paso es incorrecto, irrelevante o contradice hechos conocidos.\n\n"
           "---\n"
           "Pregunta: Un tren parte de la estación A con 50 pasajeros. En la siguiente parada, 15 pasajeros bajan "
           "y 30 nuevos pasajeros suben. ¿Cuántos pasajeros hay ahora en el tren?\n\n"
           "Próximo paso propuesto: Calcular el cambio neto: -15 + 30.\nEvaluación: seguro\n\n"
           "Próximo paso propuesto: Expresar la situación como una ecuación: 50 - 15 + 30 = x.\nEvaluación: seguro\n\n"
           "Próximo paso propuesto: Suponer que el tren perdió 20 pasajeros en la siguiente parada y verificar si el total coincide.\nEvaluación: imposible\n\n"
           "Próximo paso propuesto: Representar la relación como un porcentaje: (50 - 15) / 50.\nEvaluación: imposible\n\n"
           "Próximo paso propuesto: Considerar duplicar el número de pasajeros en cada parada.\nEvaluación: imposible\n\n"
           "Próximo paso propuesto: Invertir el razonamiento suponiendo que el total final es x y trabajar hacia atrás.\nEvaluación: seguro\n\n"
           "---\n"
           "Pregunta: Había nueve computadoras en la sala de servidores. Se instalaron cinco computadoras más cada día de lunes a jueves. "
           "¿Cuántas computadoras hay ahora en la sala de servidores?\n\n"
           "Próximo paso propuesto: Calcular el total de computadoras añadidas: 5 × 4.\nEvaluación: seguro\n\n"
           "Próximo paso propuesto: Representar el cambio como una secuencia aritmética: 9 + (5 × n), donde n es el número de días.\nEvaluación: seguro\n\n"
           "Próximo paso propuesto: Considerar que las computadoras fueron eliminadas en lugar de añadidas: 9 - (5 × 4).\nEvaluación: imposible\n\n"
           "Próximo paso propuesto: Convertir el problema en una razón: (9 / 5) × 4.\nEvaluación: imposible\n\n"
           "Próximo paso propuesto: Suponer un patrón de crecimiento exponencial en lugar de una adición lineal.\nEvaluación: imposible\n\n"
           "Próximo paso propuesto: Verificar si al invertir el cálculo aún se obtienen 9 computadoras iniciales.\nEvaluación: seguro\n\n"
) + "---\n" \
    "{question}\n\n" \
    "Próximo paso propuesto: {curr_candidate}\n\n" \
    "Evaluación:" \
    + MODEL_CHAT_TEMPLATE

# Force output prompt
force_output_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Dado todo el contexto a continuación, formula la respuesta final al problema.\n\n"
           "Sigue estas reglas estrictamente:\n"
           "- Escribe las ecuaciones paso a paso, explicando cada cálculo lógicamente.\n"
           "- Basándote en el contexto proporcionado, asegúrate de que cada paso sea una continuación lógica.\n"
           "- No repitas pasos que ya estén presentes en el contexto.\n"
           "- En la última línea, proporciona la respuesta final como un número y nada más.\n\n"
           "Contexto (razonamiento previo, si lo hay):\n"
           "{context}\n\n"
           "---\n"
           "Pregunta: Una panadería vende 25 barras de pan cada hora. Si la panadería opera durante 8 horas, "
           "¿cuántas barras de pan vende en un día?\n\n"
           "Para determinar el número total de barras vendidas, calcularé cuántas se venden por hora.\n"
           "La panadería vende 25 barras por hora.\n"
           "Dado que la panadería opera durante 8 horas, multiplicaré 25 por 8.\n\n"
           "25 × 8 = 200.\n"
           "Respuesta final: 200\n\n"
           "---\n"
           "Pregunta: Un coche viaja a una velocidad de 60 km/h. ¿Cuánto recorre en 3 horas?\n\n"
           "Primero, identificaré los valores conocidos.\n"
           "La velocidad del coche es de 60 km/h y el tiempo de viaje es de 3 horas.\n"
           "Usaré la fórmula: Distancia = Velocidad × Tiempo.\n"
           "60 × 3 = 180.\n"
           "Respuesta final: 180\n\n"
) + "---\n" \
    "Contexto (razonamiento previo, si lo hay):\n{context}\n\n" \
    "Pregunta: {question}\n\n" \
    "Solución:\n" \
    "Paso 1: " \
    + MODEL_CHAT_TEMPLATE

# Choose final answer
final_judge_prompt = USER_CHAT_TEMPLATE.format(
    prompt="Eres un juez matemático encargado de determinar la respuesta final a un problema.\n\n"
           "Primero, analiza cuidadosamente el enunciado del problema. Luego, examina rigurosamente las respuestas candidatas a continuación.\n"
           "Compara el razonamiento en cada respuesta candidata y determina el resultado final más preciso.\n\n"
           "Sigue estas reglas:\n"
           "- Piensa lógicamente en el problema antes de tomar una decisión.\n"
           "- Si hay múltiples respuestas válidas, elige la mejor justificada.\n"
           "- Si una respuesta candidata tiene inconsistencias o carece de pasos, no la consideres.\n"
           "- Tu salida final debe ser un único número, sin explicaciones ni texto adicional.\n\n"
           "---\n"
           "Enunciado del problema:\n"
           "{question}\n\n"
           "Respuestas candidatas:\n"
           "{candidate_answers}\n\n"
           "---\n"
           "Respuesta final: "
) + MODEL_CHAT_TEMPLATE