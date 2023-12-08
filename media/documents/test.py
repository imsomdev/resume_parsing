import os
import pdfplumber
import docx2txt
from openai import OpenAI
# import json
# from datetime import datetime

os.environ["OPENAI_API_KEY"] = "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"
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

path = '/media/somdev/84AE09BCAE09A82E/SentientGeeks/SentientGeeks/Resume Parsing/upload_and_parse/parse_api/parse_api/media/documents/'
result = process_files_in_folder(path)


client = OpenAI()
api = os.environ.get("OPENAI_API_KEY")

# temp_cv_list = []
for element in result:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON. And maintain same variable name and format always,"},
            {"role": "user", "content": element}
        ]
    )
print(response.choices[0].message.content)