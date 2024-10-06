import PyPDF2
import json
import re

def is_heading(text):
    # Check if text is in all uppercase letters
    return text.isupper() and bool(text.strip())

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Extract text from each page
    return text

def remove_headings_and_collect_jokes(text):
    lines = text.splitlines()
    jokes = []
    current_joke = ""
    joke_id = 1

    for line in lines:
        if is_heading(line):
            # If there's a current joke, save it before starting a new one
            if current_joke.strip():  # Avoid empty jokes
                jokes.append({"id": joke_id, "text": current_joke.strip()})
                joke_id += 1
                current_joke = ""  # Reset for the next joke
        else:
            # Accumulate lines that are not headings
            current_joke += line + " "

    # Don't forget to add the last joke if exists
    if current_joke.strip():
        jokes.append({"id": joke_id, "text": current_joke.strip()})

    return jokes

def save_to_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    pdf_path = "file.pdf"
    json_path = "output.json"

    # Step 1: Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Step 2: Remove headings and collect jokes
    jokes = remove_headings_and_collect_jokes(pdf_text)

    # Step 3: Save to JSON file
    save_to_json(jokes, json_path)

if __name__ == "__main__":
    main()
