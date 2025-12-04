import pdfplumber
from io import BytesIO
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os

def getPdfContent(data):
    
    texto = ''
    with pdfplumber.open(p:=BytesIO(data)) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
    if texto:
        return texto
    else:
            # Caso contrário: precisa de OCR
        # Criar arquivo temporário para pdf2image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            pages = convert_from_path(tmp_path)

            for img in pages:
                texto += pytesseract.image_to_string(img, lang='por') + "\n"

        finally:
            # Apagar arquivo temporário
            os.remove(tmp_path)

        return texto

def readImage(data):
    pass