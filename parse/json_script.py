import os
import pdfplumber
import docx2txt
from openai import OpenAI
import json

os.environ["OPENAI_API_KEY"] = "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"

def parse(file_content):
    def pdf_parse(content):
        text = ''
        with pdfplumber.open(content) as pdf:
            pages = pdf.pages
            for page in pages:
                text += page.extract_text()
        return text

    def docx_parse(content):
        text = docx2txt.process(content)
        return text

    def process_files(file_content):
        dump = []

        base_name, file_extension = os.path.splitext(file_content.filename)
        if file_extension.lower() == ".pdf":
            dump.append(pdf_parse(file_content))
        elif file_extension.lower() == ".docx":
            dump.append(docx_parse(file_content))

        return dump


    result = process_files(file_content)

    client = OpenAI()
    api = os.environ.get("OPENAI_API_KEY")

    rewrites = []
    for element in result:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON. And maintain same variable name and format always,"},
                {"role": "user", "content": element}
            ]
        )
        rewrites.append(json.loads(response.choices[0].message.content))

    return rewrites
