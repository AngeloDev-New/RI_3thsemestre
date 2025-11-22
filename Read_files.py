import pdfplumber
from io import BytesIO
import pytesseract
from pdf2image import convert_from_path

def getPdfContent(data):
    
    texto = ''
    with pdfplumber.open(p:=BytesIO(data)) as pdf:
        for page in pdf.pages:
            texto += page.extract_text()
    if texto:
        return texto
    else:
        paginas = convert_from_path(p)
        for img in paginas:
            texto += f'{pytesseract.image_to_string(img,lang='por')}\n' 

def readImage(data):
    pass