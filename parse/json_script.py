import os
import pdfplumber
import docx2txt
from openai import OpenAI
from datetime import datetime
import json

os.environ["OPENAI_API_KEY"] = "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"
def parse(path):
    def pdf_parse(file_path):
        text = ''
        with pdfplumber.open(file_path) as pdf:
            pages = pdf.pages
            for page in pages:
                text += page.extract_text()
        return text


    def docx_parse(file_path):
        text = docx2txt.process(file_path)
        return text


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

    # path = '/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/test2'
    result = process_files_in_folder(path)


    client = OpenAI()
    api = os.environ.get("OPENAI_API_KEY")


    for element in result:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. And maintain same variable name and format always,"},
                {"role": "user", "content": element}
            ]
        )
    res = response.choices[0].message.content
    json_res = json.loads(res)
    print(json_res)
    # Using json_data and target key found date_of_birth
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
    basic_target_key_list = ['name', 'email', 'phone']
    for target_key in basic_target_key_list:
        if find_key_value(json_res, target_key) is None:
            return ['404',f'{target_key.capitalize()}']

    target_key = 'dateOfBirth'
    dob = find_key_value(json_res, target_key)
    if dob is None:
        return '404_DOB'
    age = calculate_age(dob)

    # Validating age here
    if age <18:
        return '400_AGE'
    return json_res

