from src.ai_gateway.prompt_builder import build_prompt_extractor, build_prompt_date_validator
from ollama import chat
import time
import json

def ai_call(func, *args, max_retries=3, delay=2, **kwargs):
    for attempt in range(1, max_retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt < max_retries:
                time.sleep(delay)
            else:
                print("Número máximo de tentativas atingido.")
                return None

def response(prompt):
    response = chat(
        model='llama3.1',
        messages=[
            {"role": "system", "content": "Tu és um extrator de informações de ofertas de emprego, responde de forma objetiva."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content'].strip()

def ai_extractor(section, section_steps, description):
    prompt_parts = []

    flat_steps = flatten_steps(section_steps)
    for step in flat_steps:
        part = build_prompt_extractor(
            step["question"],
            step["style"],
            step["field"],
        )
        prompt_parts.append((step["field"], part))

    full_prompt = f"Baseia-te nesta descrição de emprego:\n{description}"
    full_prompt += "\nResponde apenas com o JSON, sem texto antes ou depois, e sem comentários. Não incluas //, # ou qualquer explicação extra. Se não souberes a resposta, preenche \"Não sei\".\n"
    full_prompt += "Dá as respostas no seguinte formato JSON:\n{\n"
    for field, _ in prompt_parts:
        full_prompt += f'  "{field}": "resposta",\n'
    full_prompt = full_prompt.rstrip(',\n') + "\n}\n\n"

    full_prompt += "Responde às seguintes questões baseadas na descrição da oferta:\n\n"
    for _, part in prompt_parts:
        full_prompt += part + "\n"
    
    full_prompt += "\nLembra-te: responde apenas com o JSON, sem texto antes ou depois, e sem comentários.\n"
    raw_response = response(full_prompt)

    try:
        return json.loads(raw_response)
    except Exception as e:
        print(f"[AI EXTRACTOR] Failed to parse JSON: {e}")
        return {}

def ai_date_fixer(value):
    prompt = build_prompt_date_validator(value)
    response_text = response(prompt)
    return response_text

def flatten_steps(steps):
    flat = []
    for step in steps:
        if "subfields" in step:
            flat.extend(flatten_steps(step["subfields"]))
        elif "question" in step and "style" in step and "field" in step:
            flat.append(step)
    return flat