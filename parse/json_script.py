import os
import pdfplumber
import docx2txt
from openai import OpenAI
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
    return json.loads(response.choices[0].message.content)

