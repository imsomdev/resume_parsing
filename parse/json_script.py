import os
import pdfplumber
import docx2txt
from openai import OpenAI
from datetime import datetime
import json
from dotenv import load_dotenv
load_dotenv()


def parse(path):
    # Extract text from pdf
    def pdf_parse(file_path):
        text = ''
        with pdfplumber.open(file_path) as pdf:
            pages = pdf.pages
            for page in pages:
                text += page.extract_text()
        return text

    # Extract text from docx
    def docx_parse(file_path):
        text = docx2txt.process(file_path)
        return text

    # Checking the file type and calling functions accordingly
    def process_files_in_folder(path):
        dump = []
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                base_name, file_extension = os.path.splitext(filename)
                if file_extension.lower() == ".pdf":
                    dump.append(pdf_parse(file_path))
                elif file_extension.lower() == ".docx":
                    dump.append(docx_parse(file_path))
        return dump

    
    result = process_files_in_folder(path)

    # Invalid file type check. Result list will be empty.
    if not result:
        return ['422', 'Unsupported!! Please Provide PDF or DOCX']
    
    # Damaged file check
    if result[0] == '':
        return ['422', 'Damaged File!!']


    client = OpenAI()
    api = os.getenv("OPENAI_API_KEY")

    # Proccessing the extracted text to make it into json format
    for element in result:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. And maintain same variable name and format always like dateOfBirth, GPA, name, address, education, phone, email. Don't make up"},
                {"role": "user", "content": element}
            ]
        )
    res = response.choices[0].message.content
    json_res = json.loads(res)
    print(json_res)
    
    # Using json_data and target key found that value is present or not
    def find_key_value(data, target_key):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    return value
                elif isinstance(value, (dict, list)):
                    result = find_key_value(value, target_key)
                    if result is not None:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = find_key_value(item, target_key)
                if result is not None:
                    return result
        return None
    
    # Calculate age using date_of_birth
    def calculate_age(date_of_birth):
        birth_date = datetime.strptime(date_of_birth, '%d/%m/%Y')
        current_date = datetime.now()
        age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        return age
    
    # Validating basic details
    basic_target_key_list = ['name', 'email', 'phone', 'dateOfBirth', 'address', 'education', 'GPA']
    details = {}
    for basic_key in basic_target_key_list:
        value = find_key_value(json_res, basic_key)
        if value is None:
            return ['404', f'{basic_key.capitalize()}']
        else:
            details[basic_key] = value

    # Validating age here
    age = calculate_age(details['dateOfBirth'])
    if age < 18:
        return ['400', 'age']

    # Validating gpa here
    if float(details['GPA']) < 3.0:
        return ['400', 'GPA']
    
    return [json_res]
