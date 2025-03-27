import os
import email
import pytesseract
from pdfminer.high_level import extract_text
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from PIL import Image
import io
import docx
import json
import xml.etree.ElementTree as ET
from fastapi import FastAPI, UploadFile, File
import uvicorn
from transformers import pipeline
import requests

app = FastAPI()
summarizer = pipeline("summarization")

def parse_email(file_path):
    with open(file_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)
    
    email_data = {
        "from": msg['From'],
        "to": msg['To'],
        "subject": msg['Subject'],
        "date": msg['Date'],
        "body": extract_email_body(msg),
        "attachments": process_attachments(msg)
    }
    
    email_data["summary"] = summarize_text(email_data["body"])
    forward_email(email_data)
    
    return email_data

def extract_email_body(msg):
    if msg.is_multipart():
        for part in msg.iter_parts():
            if part.get_content_type() == "text/html":
                return BeautifulSoup(part.get_content(), "html.parser").text
            elif part.get_content_type() == "text/plain":
                return part.get_content()
    return ""

def process_attachments(msg):
    attachments = []
    for part in msg.iter_attachments():
        file_name = part.get_filename()
        file_type = part.get_content_type()
        file_data = part.get_payload(decode=True)
        
        if not file_name:
            continue
        
        if file_type in ["text/plain", "text/csv"]:
            content = file_data.decode("utf-8", errors="ignore")
        elif file_type in ["application/json"]:
            content = json.loads(file_data.decode("utf-8", errors="ignore"))
        elif file_type in ["application/xml", "text/xml"]:
            content = extract_text_from_xml(file_data)
        elif file_type in ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/bmp"]:
            content = extract_text_from_image(file_data)
        elif file_type == "application/pdf":
            content = extract_text_from_pdf(file_data)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            content = extract_text_from_docx(file_data)
        else:
            content = "Unsupported file type"
        
        attachments.append({"file_name": file_name, "content": content})
    
    return attachments

def extract_text_from_image(image_data):
    image = Image.open(io.BytesIO(image_data))
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_data):
    with open("temp.pdf", "wb") as f:
        f.write(pdf_data)
    text = extract_text("temp.pdf")
    os.remove("temp.pdf")
    return text

def extract_text_from_docx(docx_data):
    with open("temp.docx", "wb") as f:
        f.write(docx_data)
    doc = docx.Document("temp.docx")
    text = "\n".join([para.text for para in doc.paragraphs])
    os.remove("temp.docx")
    return text

def extract_text_from_xml(xml_data):
    root = ET.fromstring(xml_data)
    return "\n".join([elem.text for elem in root.iter() if elem.text])

def summarize_text(text):
    if len(text) > 50:
        return summarizer(text[:1024], max_length=150, min_length=50, do_sample=False)[0]['summary_text']
    return text

def forward_email(email_data):
    forward_url = "http://other-team-service.com/receive-email"
    try:
        response = requests.post(forward_url, json=email_data)
        return response.status_code
    except Exception as e:
        return str(e)

@app.post("/parse-email/")
async def parse_email_api(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    email_data = parse_email(file_path)
    os.remove(file_path)
    return email_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Example Usage:
# Start the API: `uvicorn email_parser_ai:app --reload`
# Send a POST request with an `.eml` file to `http://localhost:8000/parse-email/`
