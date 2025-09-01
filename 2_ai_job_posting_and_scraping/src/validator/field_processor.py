from src.validator.business_validator import BusinessValidator
from src.uni_bot.steps_config import required_section_fields_list
from src.uni_bot.data_processor import DataProcessor

class FieldProcessor:
    def __init__(self, forms_config, options_list):
        self.business_validator = BusinessValidator(forms_config=forms_config, options_provider=options_list)
        self.options_list = options_list
        self.data_processor = DataProcessor()

    def validate_fields(self, job_fields, section):
        try:
            data = self._validator(job_fields, section)
            if data is not None:
                clean = self._cleaner(data, section)
                if clean is not None:
                    return clean
                else:
                    return {}
            else:
                print(f"No data returned from validator for section '{section}'.")
                return {}
        except Exception as e:
            print(f"An error occurred during field validation: {e}")
            return {}

    def _validator(self, job_fields, section):
        print("____________________FIELD____________________VALIDATOR____________________")
        validated_data = {}
        print(f"Validating job fields for section '{section}':", job_fields)

        try:
            section_fields = required_section_fields_list(section)
            print(f"Section {section} fields: {section_fields}")
            if section_fields and isinstance(section_fields[0], dict):
                section_fields = [f["field"] for f in section_fields]

            for field_name, field_value in job_fields.items():
                if field_name not in section_fields:
                    continue

                field_value = self._preprocess_value(field_value)

                if self.business_validator.validate(field_name, field_value):
                    validated_data[field_name] = field_value
                else:
                    if field_name in [
                        "start_date_full_time", "end_date_full_time",
                        "start_date_shift", "end_date_shift",
                        "start_date_custom", "end_date_custom"
                    ] and field_value not in ["", None] :
                        new_date = self.data_processor.date_fixer(field_value)
                        if self.business_validator.validate(field_name, new_date):
                            validated_data[field_name] = new_date
                        else:
                            validated_data[field_name] = ""
                    else:
                        validated_data[field_name] = ""

                print(f"Field '{field_name}' validated with value: {validated_data[field_name]}")

        except Exception as e:
            print(f"An error occurred during validation: {e}")
            return {}

        print(f"\nValidation result for section '{section}': {validated_data}")
        return validated_data

    def _cleaner(self, job_fields, section):
        print("____________________FIELD____________________CLEANER____________________")
        print(f"Cleaning job fields for section '{section}':", job_fields)
        job_fields_cleaned = {}

        try:
            section_fields = required_section_fields_list(section)
            print(f"Section {section} fields: {section_fields}")
            if section_fields and isinstance(section_fields[0], dict):
                section_fields = [f["field"] for f in section_fields]

            for field_name in section_fields:
                if field_name not in job_fields:
                    print(f"[DEBUG] Field '{field_name}' not in job_fields, skipping")
                    continue

                field_value = self._preprocess_value(job_fields[field_name])
                print(f"[DEBUG] Processing field '{field_name}' with value: '{field_value}' (type: {type(field_value)})")

                # Corrigir para usar sempre a função options_list
                try:
                    options = self.options_list(field_name)
                    print(f"[DEBUG] Options for field '{field_name}': {options}")
                except Exception as e:
                    print(f"Error retrieving options for field '{field_name}': {e}")
                    options = None

                if options and field_value not in options:
                    print(f"[DEBUG] Field '{field_name}' value '{field_value}' not in options {options}, setting to empty")
                    job_fields_cleaned[field_name] = ""
                    continue

                if isinstance(field_value, str) and (field_value.strip().lower() in ["não sei", ""] or "não sei" in field_value.lower()):
                    print(f"[DEBUG] Cleaning field '{field_name}' with 'não sei' value: {field_value}")
                    job_fields_cleaned[field_name] = ""
                    continue

                job_fields_cleaned[field_name] = field_value
                print(f"[DEBUG] Field '{field_name}' keeps value: {job_fields_cleaned[field_name]}")

        except Exception as e:
            print(f"An error occurred during cleaning: {e}")
            return job_fields

        return job_fields_cleaned

    def _preprocess_value(self, value):
        if isinstance(value, str):
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            value = value.rstrip(".")
        return value
