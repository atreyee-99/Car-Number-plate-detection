from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"E:\Tesseract-OCR\tesseract.exe"
image = Image.open(your_image)
image_to_text = pytesseract.image_to_string(image, lang='eng')
print(image_to_text)
