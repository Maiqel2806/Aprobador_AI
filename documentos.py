import pytesseract
import cv2
import numpy as np
import os
from pdf2image import convert_from_path
from datetime import datetime, timedelta
import re

# Configurar la ruta del ejecutable de Tesseract si es necesario
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Lista de documentos PDF a procesar
documentos = ['NOM.pdf']  # Agrega los nombres de tus documentos PDF

def extraer_texto_de_pagina(pdf_path, pagina_num):
    # Convertir la página del PDF en una imagen
    imagen = convert_from_path(pdf_path, first_page=pagina_num, last_page=pagina_num)[0]
    
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(np.array(imagen), cv2.COLOR_BGR2GRAY)
    
    # Usar pytesseract para extraer el texto de la imagen
    texto = pytesseract.image_to_string(gray)
    
    return texto

# Procesar cada documento
for documento in documentos:
    if os.path.exists(documento):
        print(f"Procesando {documento}...")
        
        # Convertir el PDF a imágenes y procesar cada página
        paginas = convert_from_path(documento)
        texto_completo = ''
        for i, pagina in enumerate(paginas):
            print(f"\nProcesando página {i + 1}...")
            texto_extraido = extraer_texto_de_pagina(documento, i + 1)
            texto_completo += texto_extraido
            
        # Mostrar el texto completo extraído del documento
        print("\nTexto completo extraído del documento:\n", texto_completo)
        
        # Verificar la condición de "SITUACIÓN ACTUAL: ACTIVA"
        if "SITUACION ACTUAL: ACTIVA" in texto_completo:
            print("La situación actual es 'ACTIVA'.")
                      
        else:
            print(f"El documento {documento} NO cumple con la condición de 'SITUACIÓN ACTUAL: ACTIVA'.")
    else:
        print(f"El archivo {documento} no se encuentra.")
