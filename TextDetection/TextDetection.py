from PIL import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

def img_str(s):
    # Image to string in spanish language
    # s = '/data/sample.png'
    pre = (pytesseract.image_to_string(Image.open(s), lang='spa'))
    nameSt = pre.index('Nombre:')
    apeSt = pre.index('Apellidos:')
    nacSt = pre.index('Fecha de nacimiento:')
    sanSt = pre.index('Tipo de sangre:')
    aleSt = pre.index('Alergias:')
    enfSt = pre.index('Enfermedades:')
    name = pre[nameSt+7:apeSt].strip().replace('_', '')
    ape = pre[apeSt+10:nacSt].strip().replace('_', '')
    nac = pre[nacSt+20:sanSt].strip().replace('_', '')
    san = pre[sanSt+15:aleSt].strip().replace('_', '')
    ale = pre[aleSt+9:enfSt].strip().replace('_', '')
    enf = pre[enfSt+13:len(pre)].strip().replace('_', '')
    return name, ape, nac, san, ale, enf
