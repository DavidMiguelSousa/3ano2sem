from src.uni_bot.steps_config import forms
from src.uni_bot.options_config import options_list
from src.validator.field_processor import FieldProcessor
from src.uni_bot.data_processor import DataProcessor

import threading

fieldProcessor = FieldProcessor(forms_config=forms, options_list=options_list)
dataProcessor = DataProcessor()

def start_forms_threads_extract(description, job_fields):
    threads = []
    lock = threading.Lock()

    def extract_section(section, fields):
        result = dataProcessor.extractor(description, fields, job_fields, section)
        with lock:
            job_fields.update(result)

    for section, fields in forms["steps"].items():
        print(f"[EXTRACT] Creating thread for section: {section}")
        thread = threading.Thread(
            target=extract_section,
            args=(section, fields)
        )
        threads.append(thread)

    print("[EXTRACT] Starting threads...")

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("[EXTRACT] All threads finished.")


def start_forms_threads_validate(job_fields_validate):
    threads = []
    validated_fields = {}

    print("job fields BEFORE validation:\n", job_fields_validate)

    lock = threading.Lock()

    def validate_section(section):
        result = fieldProcessor.validate_fields(job_fields_validate.copy(), section)
        with lock:
            job_fields_validate.update(result)

    for section in forms["steps"]:
        print(f"[VALIDATE] Creating thread for section: {section}")
        thread = threading.Thread(
            target=validate_section,
            args=(section,)
        )
        threads.append(thread)

    print("[VALIDATE] Starting threads...")

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("[VALIDATE] All threads finished.")
