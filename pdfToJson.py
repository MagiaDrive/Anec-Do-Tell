import PyPDF2
import json
import re

def is_heading(text):
    return text.isupper() and bool(text.strip())

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n" 
    return text

def remove_headings_and_collect_jokes(text):
    lines = text.splitlines()
    jokes = []
    current_joke = ""
    joke_id = 1

    for line in lines:
        if is_heading(line):
            if current_joke.strip(): 
                jokes.append({"id": joke_id, "text": current_joke.strip()})
                joke_id += 1
                current_joke = "" 
        else:
            current_joke += line + " "

    if current_joke.strip():
        jokes.append({"id": joke_id, "text": current_joke.strip()})

    return jokes

def save_to_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    pdf_path = "file.pdf"
    json_path = "output.json"

    pdf_text = extract_text_from_pdf(pdf_path)

    jokes = remove_headings_and_collect_jokes(pdf_text)

    save_to_json(jokes, json_path)

if __name__ == "__main__":
    main()
