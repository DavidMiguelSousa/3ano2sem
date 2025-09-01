from src.uni_bot.options_config import options_list

forms = {
    "sections": [
        "details",
        "location",
        "schedule_and_vacancies",
        "compensation_and_benefits"
    ],
    
    "fields": [
        "company",
        "degree_of_specialization",
        "job_title",
        "work_area",
        "job_description",
        "work_mode",
        "job_address",
        "job_country",
        "district",
        "job_city",
        "lat",
        "lng",
        "pin_code",
        "geo_radius",
        "schedule_type",
        "start_date_full_time",
        "end_date_full_time",
        "vacancies_full_time",
        "shifts",
        "shift_name",
        "start_date_shift",
        "end_date_shift",
        "vacancies_shift",
        "custom",
        "custom_shift_name",
        "start_date_custom",
        "end_date_custom",
        "vacancies_custom",
        "payment_frequency",
        "amount",
        "how_to_pay_student",
        "type_of_applicant",
        "teams_amount",
        "team_ids",
        "benefits"
    ],

    "steps": {
        "details": [
            {"field": "company", "question": "Que empresa está a oferecer o trabalho?", "prompt": lambda x: x.strip(), "style": "direct"},
            {"field": "degree_of_specialization", "question": "Nível de especialização do trabalho.", "prompt": lambda x: x.strip(), "style": "options"},
            {"field": "job_title", "question": "Qual é o cargo?", "prompt": lambda x: x.strip(), "style": "direct"},
            {"field": "work_area", "question": "Como classifica o trabalho?", "prompt": lambda x: x.strip(), "style": "options"},
            {"field": "job_description", "question": "Descreva o trabalho.", "prompt": lambda x: x.strip(), "style": "detailed"},
        ],

        "location": [
            {"field": "work_mode", "question": "Qual o modo de trabalho?", "prompt": lambda x: x.strip(), "style": "options"},
            {
                "field": "address", "subfields": [
                    {"field": "job_address", "question": "Qual é o endereço da empresa?", "prompt": lambda x: x.strip(), "style": "address"},
                    {"field": "job_country", "question": "Qual é o país?", "prompt": lambda x: x.strip(), "style": "direct"},
                    {"field": "district", "question": "Qual é o distrito?", "prompt": lambda x: x.strip(), "style": "direct"},
                    {"field": "job_city", "question": "Qual é a cidade?", "prompt": lambda x: x.strip(), "style": "direct"},
                    {"field": "lat", "question": "Qual é a latitude?", "prompt": lambda x: x.strip(), "style": "numeric"},
                    {"field": "lng", "question": "Qual é a longitude?", "prompt": lambda x: x.strip(), "style": "numeric"},
                    {"field": "pin_code", "question": "Qual é o código postal?", "prompt": lambda x: x.strip(), "style": "direct"},
                ]
            },
            {"field": "geo_radius", "question": "Qual é o raio geográfico para um trabalhador dar clock-in/clock-out? (em metros)", "prompt": lambda x: x.strip(), "style": "numeric"},
        ],

        "schedule_and_vacancies": [
            {"field": "schedule_type", "question": "Qual é o plano de trabalho?", "prompt": lambda x: x.strip(), "style": "options"},
            {
                "field": "full_time", "subfields": [
                    {"field": "start_date_full_time", "question": "O trabalho começa em que dia?", "prompt": lambda x: x.strip(), "style": "date"},
                    {"field": "end_date_full_time", "question": "O trabalho termina em que dia?", "prompt": lambda x: x.strip(), "style": "date"},
                    {"field": "vacancies_full_time", "question": "Quantas vagas estão disponíveis?", "prompt": lambda x: x.strip(), "style": "numeric"},
                ]
            },
            {
                "field": "weekly_shift", "subfields": [
                    {"field": "shifts", "question": "Quantos turnos vão haver?", "prompt": lambda x: x.strip(), "style": "numeric"},
                    {
                        "field": "shift", "subfields": [
                            {"field": "shift_name", "question": "Qual é o nome do turno?", "prompt": lambda x: x.strip(), "style": "direct"},
                            {"field": "start_date_shift", "question": "Este turno começa em que dia?", "prompt": lambda x: x.strip(), "style": "date"},
                            {"field": "end_date_shift", "question": "Este turno termina em que dia?", "prompt": lambda x: x.strip(), "style": "date"},
                            {"field": "vacancies_shift", "question": "Quantas vagas estão disponíveis para o turno?", "prompt": lambda x: x.strip(), "style": "numeric"},
                        ]
                    }
                ]
            },
            {
                "field": "custom", "subfields": [
                    {"field": "custom_shift_name", "question": "Qual é o nome do turno?", "prompt": lambda x: x.strip(), "style": "direct"},
                    {"field": "start_date_custom", "question": "Este turno começa em que dia?", "prompt": lambda x: x.strip(), "style": "date"},
                    {"field": "end_date_custom", "question": "Este turno termina em que dia?", "prompt": lambda x: x.strip(), "style": "date"},
                    {"field": "vacancies_custom", "question": "Quantas vagas estão disponíveis para o turno?", "prompt": lambda x: x.strip(), "style": "numeric"},
                ]
            },
        ],

        "compensation_and_benefits": [
            {"field": "payment_frequency", "question": "Qual é a frequência de pagamento?", "prompt": lambda x: x.strip(), "style": "options"},
            {"field": "amount", "question": "Quanto vai pagar?", "prompt": lambda x: x.strip(), "style": "numeric"},
            {"field": "how_to_pay_student", "question": "Forma de pagamento?", "prompt": lambda x: x.strip(), "style": "options"},
            {"field": "type_of_applicant", "question": "Trabalho destinado a quem?", "prompt": lambda x: x.strip(), "style": "options"},
            {"field": "teams_amount", "question": "Quantas equipas são?", "prompt": lambda x: x.strip(), "style": "direct"},
            {"field": "team_ids", "question": "Quais são as equipa?", "prompt": lambda x: x.strip(), "style": "direct"},
            {"field": "benefits", "question": "Benefícios?", "prompt": lambda x: x.strip(), "style": "detailed"},
        ],
    },
    
    "rules": [
        {"field": "company", "value": "text"},
        {"field": "degree_of_specialization", "value": "options"},
        {"field": "work_area", "value": "options"},
        {"field": "job_title", "value": "text"},
        {"field": "job_description", "value": "detailed"},
        {"field": "work_mode", "value": "options"},
        {"field": "job_address", "value": "address"},
        {"field": "job_country", "value": "text"},
        {"field": "district", "value": "text"},
        {"field": "job_city", "value": "text"},
        {"field": "lat", "value": "numeric"},
        {"field": "lng", "value": "numeric"},
        {"field": "pin_code", "value": "postal_code"},
        {"field": "geo_radius", "value": "numeric"},
        {"field": "schedule_type", "value": "options"},
        {"field": "start_date_full_time", "value": "date"},
        {"field": "end_date_full_time", "value": "date"},
        {"field": "vacancies_full_time", "value": "numeric"},
        {"field": "shifts", "value": "numeric"},
        {"field": "shift_name", "value": "text"},
        {"field": "start_date_shift", "value": "date"},
        {"field": "end_date_shift", "value": "date"},
        {"field": "vacancies_shift", "value": "numeric"},
        {"field": "custom", "value": "text"},
        {"field": "custom_shift_name", "value": "text"},
        {"field": "start_date_custom", "value": "date"},
        {"field": "end_date_custom", "value": "date"},
        {"field": "vacancies_custom", "value": "numeric"},
        {"field": "payment_frequency", "value": "options"},
        {"field": "amount", "value": "numeric"},
        {"field": "how_to_pay_student", "value": "options"},
        {"field": "type_of_applicant", "value": "options"},
        {"field": "teams_amount", "value": "numeric"},
        {"field": "team_ids", "value": "text"},
        {"field": "benefits", "value": "Benefícios não especificados"},
    ],

    "required_fields": {
        "details": [
            "company",
            "degree_of_specialization",
            "job_title",
            "job_description",
            "work_area"
        ],
        "location": [
            "work_mode",
            "job_address",
            "job_country",
            "district",
            "job_city",
            "lat",
            "lng",
            "pin_code",
            "geo_radius"
        ],
        "schedule_and_vacancies": {
            "base": [
                "schedule_type",
            ],
            "advanced": {
                "full-time": [
                    "start_date_full_time",
                    "end_date_full_time",
                    "vacancies_full_time"
                ],
                "part-time": [
                    "shifts",
                    "shift_name",
                    "start_date_shift",
                    "end_date_shift",
                    "vacancies_shift"
                ],
                "custom": [
                    "custom_shift_name",
                    "start_date_custom",
                    "end_date_custom",
                    "vacancies_custom"
                ]
            },
        },
        "compensation_and_benefits": {
            "base": [
                "payment_frequency",
                "amount",
                "how_to_pay_student",
                "type_of_applicant",
                "benefits"
            ],
            "advanced": {
                "team-only": [
                    "teams_amount", 
                    "team_ids"
                ]
            },
        },
    },
}

from datetime import datetime
import random

def get_today_date():
    return datetime.today().strftime('%d/%m/%Y')

def select_random_option(field):
    options = options_list(field)
    if not options:
        print(f"⚠️ [select_random_option] No options found for field: {field}")
        return None
    
    return random.choice(options)

default_values = [
    {"field": "company", "value": "Company David"},
    {"field": "degree_of_specialization", "value": "Non-specialized"},
    {"field": "work_area", "value": "Catering"},
    {"field": "job_title", "value": "Título do trabalho"},
    {"field": "job_description", "value": "Descrição do trabalho não especificada."},
    {"field": "work_mode", "value": "On-site"},
    {"field": "job_address", "value": "Rua Exemplo, 123"},
    {"field": "job_country", "value": "Portugal"},
    {"field": "district", "value": "Porto"},
    {"field": "job_city", "value": "Porto"},
    {"field": "lat", "value": "0"},
    {"field": "lng", "value": "0"},
    {"field": "pin_code", "value": "1000-000"},
    {"field": "geo_radius", "value": "50"},
    {"field": "schedule_type", "value": "Full-time"},
    {"field": "start_date_full_time", "value": get_today_date()},
    {"field": "end_date_full_time", "value": get_today_date()},
    {"field": "vacancies_full_time", "value": "1"},
    {"field": "shifts", "value": "1"},
    {"field": "shift_name", "value": "Não definido"},
    {"field": "start_date_shift", "value": get_today_date()},
    {"field": "end_date_shift", "value": get_today_date()},
    {"field": "vacancies_shift", "value": "1"},
    {"field": "custom_shift_name", "value": "Não definido"},
    {"field": "start_date_custom", "value": get_today_date()},
    {"field": "end_date_custom", "value": get_today_date()},
    {"field": "vacancies_custom", "value": "1"},
    {"field": "payment_frequency", "value": "Monthly"},
    {"field": "amount", "value": "1000"},
    {"field": "how_to_pay_student", "value": "Green Receipts"},
    {"field": "type_of_applicant", "value": "Public"},
    {"field": "teams_amount", "value": "1"},
    {"field": "team_ids", "value": "1"},
    {"field": "benefits", "value": "Benefícios não especificados"},
]

def required_section_fields_list(section):
    required_fields = []
    
    if section in forms["sections"]:
        if isinstance(forms["required_fields"][section], list):
            required_fields.extend(forms["required_fields"][section])
        elif isinstance(forms["required_fields"][section], dict):
            required_fields.extend(forms["required_fields"][section]["base"])
            if "advanced" in forms["required_fields"][section]:
                for advanced_section in forms["required_fields"][section]["advanced"]:
                    required_fields.extend(forms["required_fields"][section]["advanced"][advanced_section])
                    
    return required_fields


def get_field_question(field_name):
    for section in forms["sections"]:
        if section in forms["steps"]:
            for field in forms["steps"][section]:
                if field["field"] == field_name:
                    return field["question"]
                if "subfields" in field:
                    for subfield in field["subfields"]:
                        if subfield["field"] == field_name:
                            return subfield["question"]
    return None