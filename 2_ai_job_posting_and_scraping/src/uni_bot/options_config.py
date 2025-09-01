options_mapping = {
    "degreeOfSpecialization": ["Specialized", "Non-specialized"],
    "workArea": ["Bar Service", "Promotion & Brand Activation", "Tutoring", "Catering"],
    "workMode": ["Remote", "On-site", "Hybrid"],
    "scheduleType": ["Full-Time", "Part-Time", "Custom"],
    "payment_frequency": ['Monthly','Hourly','Per-Shift','Agreement'],
    "how_to_pay_student": ["(Select All)", "Green Receipts", "Isolated Acts", "Employment Contract", "Other"],
    "type_of_applicant": ['Public','Team-only'],
    "locations": [
        "Outro",
        "Lisboa",
        "Porto",
        "Setúbal",
        "Braga",
        "Viseu",
        "Aveiro",
        "Coimbra",
        "R. A. Madeira",
        "Vila Real",
        "Faro",
        "Guarda",
        "Beja",
        "Bragança",
        "Castelo Branco",
        "Leiria",
        "Portalegre",
        "Santarém",
        "Viana do Castelo",
        "Évora",
        "R. A. Açores",
    ]
}

def options_list(field_name):
    # Usa o nome do campo diretamente, tenta snake_case e camelCase
    if field_name in options_mapping:
        return options_mapping[field_name]
    # tenta camelCase se não encontrar em snake_case
    camel_case = ''.join(word.capitalize() if i > 0 else word for i, word in enumerate(field_name.split('_')))
    if camel_case in options_mapping:
        return options_mapping[camel_case]
    return []

def fix_options(value, field):
    if not value:
        return ""

    if value == []:
        return ""

    options = options_list(field)
    normalized_value = str(value).lower().strip()
    normalized_options = [opt.lower() for opt in options]

    if normalized_value not in normalized_options:
        return ""

    index = normalized_options.index(normalized_value)
    return options[index]