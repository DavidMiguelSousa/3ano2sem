import json
from datetime import datetime
from src.uni_bot.options_config import fix_options, options_list

class JobModelFromBot():
    def __init__(self, data):
        self.job_title = data.get('job_title')
        self.degree_of_specialization = fix_options(data.get('degree_of_specialization'), "degreeOfSpecialization")
        self.area_of_work_id = get_index(fix_options(data.get('work_area'), "workArea"), "workArea")
        self.job_description = data.get('job_description')
        self.work_mode = fix_options(data.get('work_mode'), "workMode")

        address = form_address(data.get('job_address'), data.get('job_country'), data.get('job_city'))
        self.job_address = address
        self.job_latitude = safe_get_coordinate(data.get('lat'))
        self.job_longitude = safe_get_coordinate(data.get('lng'))
        self.post_code = data.get('pin_code')
        self.geofencing_radius = safe_get_int(data.get('geo_radius'), 50)

        self.schedule_type = fix_options(data.get('schedule_type'), "scheduleType")
        self.schedule = get_schedule_data(data)
        # Fallback logic for job_start_date and job_end_date
        self.job_start_date = format_date((
            data.get('job_start_date') or
            data.get('start_date_full_time') or
            extract_start_date(data)
        ))
        self.job_end_date = format_date((
            data.get('job_end_date') or
            data.get('end_date_full_time') or
            extract_end_date(data)
        ))

        payment_freq = fix_options(data.get('payment_frequency'), "paymentFrequency")
        self.payment_frequency = payment_freq.lower() if payment_freq else payment_freq
        amount = str(data.get('amount') or '').replace('€', '')
        self.amount = 0 if self.payment_frequency == 'agreement' else safe_get_amount(amount)
        type_of_applicant_val = fix_options(data.get('type_of_applicant'), "typeOfApplicant")
        self.type_of_applicant = type_of_applicant_val.lower() if type_of_applicant_val else type_of_applicant_val
        self.benefits = data.get('benefits')

        self.location_id = {
            "value": get_index(data.get('location_id'), "locations"),
            "label": data.get('location_id')
        }
        payment_method = fix_options(data.get('how_to_pay_student'), "howToPayStudent")
        self.how_to_pay_student = [{
            "id": get_index(payment_method, "howToPayStudent"),
            "label": payment_method,
            "value": payment_method
        }] if payment_method else []
        self.teams = data.get('team_Ids', '').strip()

    def to_dict(self):
        return {
            "job_title": self.job_title,
            "degree_of_specialization": self.degree_of_specialization.lower() if self.degree_of_specialization else None,
            "area_of_work_id": self.area_of_work_id,
            "job_description": self.job_description,
            "work_mode": self.work_mode.lower() if self.work_mode else None,
            "job_address": self.job_address,
            "job_latitude": self.job_latitude,
            "job_longitude": self.job_longitude,
            "post_code": self.post_code,
            "geofencing_radius": self.geofencing_radius,
            "schedule_type": self.schedule_type.lower() if self.schedule_type else None,
            "payment_frequency": self.payment_frequency if self.payment_frequency else None,
            "amount": self.amount,
            "type_of_applicant": self.type_of_applicant,
            "benefits": self.benefits,
            "job_start_date": self.job_start_date if isinstance(self.job_start_date, str) else (self.job_start_date.isoformat() if self.job_start_date else None),
            "job_end_date": self.job_end_date if isinstance(self.job_end_date, str) else (self.job_end_date.isoformat() if self.job_end_date else None),
            "location_id": self.location_id,
            "how_to_pay_student": self.how_to_pay_student,
            "teams": self.teams,
            "schedule": json.dumps(self.schedule) if self.schedule else None
        }
        
class JobModelFromScraper:
    def __init__(self, data):
        print("JobModelFromScraper initialized with data:", data)
        self.job_title = data.get('job_title')
        self.degree_of_specialization = {
            "code": fix_options(data.get('degree_of_specialization'), "degreeOfSpecialization").lower(),
            "name": fix_options(data.get('degree_of_specialization'), "degreeOfSpecialization")
        }
        self.area_of_work_id = {
            "code": get_index(fix_options(data.get('work_area'), "workArea"), "workArea"),
            "name": fix_options(data.get('work_area'), "workArea")
        }
        self.job_description = data.get('job_description')
        self.work_mode = {
            "code": fix_options(data.get('work_mode'), "workMode").lower(),
            "name": fix_options(data.get('work_mode'), "workMode")
        }
        self.job_address = data.get('job_address')
        self.job_country = data.get('job_country')
        self.job_city = data.get('job_city')
        self.job_latitude = safe_get_coordinate(data.get('lat'))
        self.job_longitude = safe_get_coordinate(data.get('lng'))
        self.post_code = data.get('pin_code')
        self.district = {
            "code": get_index(fix_options(data.get('district'), "locations"), "locations"),
            "name": fix_options(data.get('district'), "locations"),
        }
        self.geofencing_radius = safe_get_int(data.get('geo_radius'))
        schedule_type_val = fix_options(data.get('schedule_type'), "scheduleType")
        if schedule_type_val and "part-time" in schedule_type_val.lower():
            schedule_type_val = "Weekly"
        self.schedule_type = {
            "code": schedule_type_val.lower() if schedule_type_val else None,
            "name": schedule_type_val.replace('-', ' ') if schedule_type_val else None
        }
        self.schedule = get_schedule_data(data)
        self.job_start_date = (
            data.get('job_start_date') or
            data.get('start_date_full_time') or
            extract_start_date(data)
        )
        self.job_end_date = (
            data.get('job_end_date') or
            data.get('end_date_full_time') or
            extract_end_date(data)
        )
        self.payment_frequency = {
            "code": fix_options(data.get('payment_frequency'), "paymentFrequency").lower(),
            "name": fix_options(data.get('payment_frequency'), "paymentFrequency"),
        }
        self.benefits = data.get('benefits')
        self.amount = data.get('amount')
        payment_method = fix_options(data.get('how_to_pay_student'), "howToPayStudent")
        self.how_to_pay_student = [{
            "id": get_index(payment_method, "howToPayStudent") or '',
            "code": payment_method,
            "name": payment_method
        }] if payment_method else []
        self.type_of_applicant = {
            "code": fix_options(data.get('type_of_applicant'), "typeOfApplicant").lower(),
            "name": fix_options(data.get('type_of_applicant'), "typeOfApplicant")
        }
        self.teams = data.get('teams', '').strip()

    def to_dict(self):
        return {
            "degreeOfSpecialization": self.degree_of_specialization if self.degree_of_specialization else None,
            "jobTitle": self.job_title,
            "areaOfWorkId": self.area_of_work_id,
            "jobDescription": self.job_description,
            "workMode": self.work_mode if self.work_mode else None,
            "jobAddress": self.job_address,
            "lat": self.job_latitude,
            "lng": self.job_longitude,
            "district": self.district,
            "geoRadius": self.geofencing_radius,
            "scheduleType": self.schedule_type,
            "jobAddress": self.job_address,
            "fullAddress":{
                "country": self.job_country,
                "city": self.job_city,
                "zipCode": self.post_code,
            },
            "fullTime": {
                "startDate": self.schedule.get('start_date') if self.schedule else None,
                "endDate": self.schedule.get('end_date', self.job_end_date) if self.schedule else None,
                "vacancies": self.schedule.get('vacancies', 1) if self.schedule else 1
            },
            "weekly": [
                {
                    "shiftName": self.schedule.get('shiftName', self.schedule_type) if self.schedule else self.schedule_type,
                    "startDate": self.schedule.get('start_date', self.job_start_date) if self.schedule else None,
                    "endDate": self.schedule.get('end_date', self.job_end_date) if self.schedule else None,
                    "vacancies": self.schedule.get('vacancies', 1) if self.schedule else 1
                }
            ],
            "customShift": {
                "shiftName": self.schedule.get('shiftName', self.schedule_type) if self.schedule else self.schedule_type,
                "startDate": self.schedule.get('start_date', self.job_start_date) if self.schedule else None,
                "endDate": self.schedule.get('end_date', self.job_end_date) if self.schedule else None,
                "vacancies": self.schedule.get('vacancies', 1) if self.schedule else 1
            },
            "payment_frequency": self.payment_frequency,
            "amount": self.amount,
            "benefits": self.benefits,
            "how_to_pay_student": self.how_to_pay_student,
            "type_of_applicant": self.type_of_applicant,
        }

def format_date(date_value):
    if not date_value:
        return None
    try:
        if "/" in date_value:
            date_obj = datetime.strptime(date_value, "%d/%m/%Y")
        elif "-" in date_value:
            date_obj = datetime.strptime(date_value, "%Y-%m-%d")
        else:
            return None
        return date_obj.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def get_index(value, field):
    options = options_list(field)
    if not isinstance(options, list):
        return None

    if value in options:
        if not field == "howToPayStudent":
            return options.index(value) + 1
        
        return options.index(value)
    else:
        return 0
    
def form_address(address, country, city):
    address = address or ""
    if not address:
        address = f"{city}, {country}" if city and country else f"{city or country}"
    
    if city and city not in address:
        address = f"{address}, {city}"
    if country and country not in address:
        address = f"{address}, {country}"
    
    return address.strip(", ")
        
def get_schedule_data(data):
    schedule_str = data.get('schedule')
    if not schedule_str:
        return get_legacy_schedule_data(data)

    try:
        schedule_data = json.loads(schedule_str)
        if not schedule_data:
            return None

        shift = schedule_data
        return {
            "shiftName": shift.get('shiftName', data.get('schedule_type')),
            "start_date": shift.get('startDate'),
            "end_date": shift.get('endDate'), 
            "vacancies": int(shift.get('vacancies', 1))
        }
    except (json.JSONDecodeError, AttributeError, IndexError) as e:
        print(f"Error parsing schedule data: {e}")
        return None

def get_legacy_schedule_data(data):
    schedule_type = data.get('scheduleType') or data.get('schedule_type')
    def safe_int(val, default=1):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default

    if schedule_type == "Full-time":
        name = schedule_type
        start = parse_date(data.get('startDateFullTime'))
        end = parse_date(data.get('endDateFullTime'))
        vacancies = safe_int(data.get('vacanciesFullTime'), 1)
    elif schedule_type == "Part-time":
        name = data.get('shiftName')
        start = parse_date(data.get('startDatePartTime'))
        end = parse_date(data.get('endDatePartTime'))
        vacancies = safe_int(data.get('vacanciesPartTime'), 1)
    else:
        name = data.get('customShiftName')
        start = parse_date(data.get('startDateCustom'))
        end = parse_date(data.get('endDateCustom'))
        vacancies = safe_int(data.get('vacanciesCustom'), 1)

    return {
        "shiftName": name,
        "start_date": start,
        "end_date": end,
        "vacancies": vacancies
    }

def parse_date(date_str, fmt='%d/%m/%Y'):
    try:
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        except ValueError:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
    except (ValueError, TypeError):
        return None

def extract_start_date(data):
    schedule = data.get("schedule")
    if not schedule:
        return None
    
    # If schedule is a string, try to parse it as JSON
    if isinstance(schedule, str):
        try:
            schedule = json.loads(schedule)
        except (json.JSONDecodeError, TypeError):
            return None
    
    # If schedule is now a dict, get the start_date
    if isinstance(schedule, dict) and schedule.get('start_date'):
        return datetime.strptime(schedule['start_date'], '%Y-%m-%d').date()
    
    return None

def extract_end_date(data):
    schedule = data.get("schedule")
    if not schedule:
        return None
    
    # If schedule is a string, try to parse it as JSON
    if isinstance(schedule, str):
        try:
            schedule = json.loads(schedule)
        except (json.JSONDecodeError, TypeError):
            return None
    
    # If schedule is now a dict, get the end_date
    if isinstance(schedule, dict) and schedule.get('end_date'):
        return datetime.strptime(schedule['end_date'], '%Y-%m-%d').date()
    
    return None

def safe_get_amount(value):
    try:
        if value:
            value = (str(value or '')).replace('€', '')
            return float(value) if value.replace('.', '', 1).isdigit() else None
        return None
    except ValueError:
        return None

def safe_get_coordinate(value):
    try:
        return float(value) if value and str(value).replace('-','').replace('.', '', 1).isdigit() else None
    except ValueError:
        return None

def safe_get_int(value, default=50):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default