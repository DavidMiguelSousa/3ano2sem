from src.uni_bot.options_config import options_list

def build_prompt_intent_recognizer(message, all_labels):
    labels = ", ".join(all_labels)
    return f"""
Mensagem: "{message}"

Classifica a mensagem de acordo com uma das seguintes intenções: {labels}.

Responde apenas com o nome da intenção, sem explicações, sem frases completas, só o nome da intenção.
"""

def build_prompt_date_validator(value):
    return f'''
Valida a seguinte data: "{value}"
Apenas responde com a data no formato dd/mm/aaaa, tens de a formatar. Se a data já estiver correta, repete-a. Se não souber ou não for válida, não expliques.
Resposta:'''


def build_prompt_extractor(question, style, field):
    if style == "direct":  
        question_styled = f"""
{question} (Responde apenas com a resposta direta e sem explicações.)
"""
    elif style == "detailed":
        question_styled = f"""
{question} (Responde com uma explicação clara e assertiva, se possível.)
"""
    elif style == "numeric":
        question_styled = f"""
{question} (Responde com um valor numérico.)
"""
    elif style == "date":
        question_styled = f"""
{question} (Responde com uma data no formato: dd/mm/aaaa.)
"""
    elif style == "options":
        if field is None:
            raise ValueError("O 'field_name' é obrigatório para perguntas de opções.")

        question_styled = f"""
{question} (Responde exatamente com uma das seguintes opções: {', '.join(options_list(field_name=field))}.
"""
    elif style == "address":
        question_styled = f"""
{question} (Responde objetivamente com o endereço completo (rua, número, cidade e/ou código postal).)
"""
    else:
        question_styled = f"""
Pergunta: {question}
"""

    return question_styled