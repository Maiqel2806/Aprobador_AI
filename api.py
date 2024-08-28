from flask import Flask, request, jsonify
import pytesseract
import cv2
import numpy as np
import os
from pdf2image import convert_from_path

app = Flask(__name__)

# Configurar la ruta del ejecutable de Tesseract si es necesario
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def extraer_texto_de_pagina(pdf_path, pagina_num):
    imagen = convert_from_path(pdf_path, first_page=pagina_num, last_page=pagina_num)[0]
    gray = cv2.cvtColor(np.array(imagen), cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gray)
    return texto

@app.route('/procesar_pdf', methods=['POST'])
def procesar_pdf():
    file = request.files['file']
    if not file:
        return jsonify({'mensaje': 'No se ha proporcionado ningún archivo.'}), 400

    archivo_path = 'temp.pdf'
    file.save(archivo_path)
    
    try:
        paginas = convert_from_path(archivo_path)
        texto_completo = ''
        for i, pagina in enumerate(paginas):
            texto_extraido = extraer_texto_de_pagina(archivo_path, i + 1)
            texto_completo += texto_extraido

        # Verificar las condiciones
        condicion1 = "SITUACION ACTUAL: ACTIVA" in texto_completo
        condicion2 = "cargo de GERENTE GENERAL" in texto_completo

        if condicion1 and condicion2:
            mensaje = "El documento cumple con ambas condiciones."
        elif condicion1:
            mensaje = "El documento cumple con la condición de 'SITUACION ACTUAL: ACTIVA', pero NO cumple con la condición de 'cargo de GERENTE GENERAL'."
        elif condicion2:
            mensaje = "El documento cumple con la condición de 'cargo de GERENTE GENERAL', pero NO cumple con la condición de 'SITUACION ACTUAL: ACTIVA'."
        else:
            mensaje = "El documento NO cumple con ninguna de las condiciones."

        return jsonify({'mensaje': mensaje})

    finally:
        os.remove(archivo_path)

if __name__ == '__main__':
    app.run(debug=True)
