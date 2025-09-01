import re
from src.uni_bot.steps_config import forms
from src.uni_bot.options_config import options_list

class BusinessValidator:
    def __init__(self, forms_config=forms, options_provider=options_list):
        self.forms = forms_config
        self.options_list = options_provider

    def validate(self, field_name, field_value):
        print(f"Validating field: {field_name} -> {field_value}")
        rule = next((r["value"] for r in self.forms["rules"] if r["field"] == field_name), None)
        print(f"rule: {rule}")

        if rule is None:
            print(f"Field '{field_name}' not found in rules.")
            return False

        match rule:
            case "options":
                return self._options_validator(field_value, field_name)
            case "postal_code":
                return self._postal_code_validator(field_value)
            case "numeric":
                return self._numeric_validator(field_value)
            case "date":
                return self._date_validator(field_value)
            case _:
                return self._text_validator(field_value)

    def _text_validator(self, value):
        return bool(value and str(value).strip() != "")

    def _options_validator(self, value, field_name):
        options = self.options_list(field_name)
        return value in options

    def _postal_code_validator(self, value):
        if not value:
            return False
        clean_value = value.replace("-", "")
        return clean_value.isdigit()

    def _numeric_validator(self, value):
        if not value:
            return False
        val = str(value).replace("€", "").replace(",", "").strip()
        # Só aceita se for só dígitos (ou float válido), sem letras
        if not re.match(r'^-?\d+(\.\d+)?$', val):
            return False
        try:
            float(val)
            return True
        except ValueError:
            return False

    def _date_validator(self, value):
        if not value:
            return False
        pattern = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        return bool(re.match(pattern, value))
