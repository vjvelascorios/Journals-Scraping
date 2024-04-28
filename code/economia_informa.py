# Scrapper de journals libres que se encuentran en la web en formato pdf y de páginas con html que contienen artículos de revistas científicas.
# El objetivo es obtener los metadatos de los artículos y el texto completo de los mismos.

# a) Scraping de páginas de internet

# 1. Seleccionar una página web que contenga artículos de revistas científicas.

## Economía Informa

# 2. Identificar los elementos de la página que contienen los metadatos de los artículos y el texto completo de los mismos.
# 3. Hacer la solicitud de información a la página web.
# 4. Realizar el scraping de la página para obtener los metadatos de los artículos y el texto completo de los mismos.
# 5. Guardar los metadatos de los artículos en un archivo csv y el texto completo de los mismos en un archivo txt.




import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger
import re


# Función para descargar los PDFs
# cSpell:ignore publicareneconinfo pdfs econinfo

def descargar_pdf(url, nombre_archivo):
    if not os.path.exists(nombre_archivo):  # Verificar si el archivo ya existe
        try:
            response = requests.get(url, timeout=(5, 30))  # Establecer un tiempo de espera para la conexión y la respuesta
            if response.status_code == 200:  # Verificar que la descarga sea exitosa
                with open(nombre_archivo, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Error al descargar el PDF desde {url}")
        except requests.exceptions.Timeout:
            print(f"Tiempo de espera agotado al intentar descargar el PDF desde {url}")
    else:
        print(f"El archivo {nombre_archivo} ya existe, omitiendo la descarga.")

# Función para obtener los enlaces a los PDFs de un número de la revista
def obtener_enlaces_pdf(url_numero):
    """
    Obtiene los enlaces a archivos PDF de una página web.

    Args:
        url_numero (str): La URL de la página web.

    Returns:
        list: Una lista de diccionarios que contienen la URL y el título de cada enlace PDF encontrado.
    """
    try:
        response = requests.get(url_numero, timeout=(5, 30))  # Establecer un tiempo de espera para la conexión y la respuesta
        soup = BeautifulSoup(response.text, 'html.parser')
        enlaces_pdf = []
        base_url = 'http://www.economia.unam.mx'
        for enlace in soup.find_all('a', href=True):
            if enlace['href'].endswith('.pdf') and "publicareneconinfo.pdf" not in enlace['href'] and "PDI.pdf" not in enlace['href']:
                enlaces_pdf.append({
                    'url': base_url + enlace['href'],
                    'titulo': enlace.text.strip()  # Utilizar el texto del enlace como título del artículo
                })
        return enlaces_pdf
    except requests.exceptions.Timeout:
        print(f"Tiempo de espera agotado al intentar obtener los enlaces PDF desde {url_numero}")
        return []

# Limpiar el texto del título del artículo para que sea un nombre de archivo válido
def limpiar_nombre_archivo(texto):
    texto = re.sub(r'[\\/*?:"<>|]', '', texto)  # Eliminar caracteres no permitidos en nombres de archivo
    texto = re.sub(r'[^\x00-\x7F]+', '', texto)  # Eliminar caracteres no ASCII
    return texto[:100]  # Limitar la longitud del nombre del archivo a 100 caracteres

# Obtener la página índice
url_indice = 'http://www.economia.unam.mx/publicaciones/econinforma/wanteriores/anteriorl.html'
try:
    response_indice = requests.get(url_indice, timeout=(5, 30))  # Establecer un tiempo de espera para la conexión y la respuesta
    soup_indice = BeautifulSoup(response_indice.text, 'html.parser')
except requests.exceptions.Timeout:
    print(f"Tiempo de espera agotado al intentar obtener la página índice desde {url_indice}")

# Crear un directorio para guardar los PDFs descargados
if not os.path.exists('pdfs_econinfo'):
    os.makedirs('pdfs_econinfo')

# Recorrer los enlaces a los números de la revista en la página índice
for enlace_numero in soup_indice.find_all('a', href=True):
    if enlace_numero['href'].startswith('/assets/pdfs/econinfo/'):
        numero = enlace_numero.text.strip()
        url_numero = f"http://www.economia.unam.mx{enlace_numero['href']}"
        print(f"Descargando número {numero}...")
        
        # Obtener los enlaces a los PDFs de este número
        enlaces_pdf = obtener_enlaces_pdf(url_numero)

        # Crear un directorio para guardar los PDFs de este número
        nombre_directorio = f"pdfs_econinfo/{numero}"
        if not os.path.exists(nombre_directorio):
            os.makedirs(nombre_directorio)

        # Descargar cada PDF del número
        merger = PdfMerger()  # Inicializar el merger para el número actual
        for idx, enlace_pdf in enumerate(enlaces_pdf):
            titulo = limpiar_nombre_archivo(enlace_pdf['titulo'])
            nombre_archivo = f"{nombre_directorio}/{numero}_{idx + 1}_{titulo}.pdf"
            descargar_pdf(enlace_pdf['url'], nombre_archivo)
            print(f"Descargando {titulo}...")
            # Verificar que el archivo PDF se descargó correctamente antes de agregarlo al merger
            if os.path.isfile(nombre_archivo):
                merger.append(nombre_archivo)
            
        # Guardar el PDF combinado para este número
        nombre_pdf_combinado = f"pdfs_econinfo/{numero}.pdf"
        with open(nombre_pdf_combinado, 'wb') as f:
            merger.write(f)
        merger.close()
        print(f"PDF combinado para el número {numero} guardado correctamente.")

print("Todos los números de la revista han sido descargados y combinados.")



# solo descarga hasta el número 383, no se puede descargar el número 382

# cambios de patrones
# 439-383
# http://www.economia.unam.mx/assets/pdfs/econinfo/439/
# http://www.economia.unam.mx/assets/pdfs/econinfo/383/

# 383-369
# http://www.economia.unam.mx/assets/pdfs/econinfo/383/
# http://www.economia.unam.mx/publicaciones/econinforma/369/

# 368-367
# http://www.economia.unam.mx/publicaciones/nueva/econinforma/368.html
# http://www.economia.unam.mx/publicaciones/nueva/econinforma/367.html

# 366-343
# http://www.economia.unam.mx/publicaciones/econinforma/366.html
# http://www.economia.unam.mx/publicaciones/econinforma/343.html





# tested
# @title Funciona
import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger
import re


# Función para descargar los PDFs
def descargar_pdf(url, nombre_archivo):
    if not os.path.exists(nombre_archivo):  # Verificar si el archivo ya existe
        try:
            response = requests.get(url, timeout=(5, 30))  # Establecer un tiempo de espera para la conexión y la respuesta
            if response.status_code == 200:  # Verificar que la descarga sea exitosa
                with open(nombre_archivo, 'wb') as f:
                    f.write(response.content)
            else:
                print(f"Error al descargar el PDF desde {url}")
        except requests.exceptions.Timeout:
            print(f"Tiempo de espera agotado al intentar descargar el PDF desde {url}")
    else:
        print(f"El archivo {nombre_archivo} ya existe, omitiendo la descarga.")

# Función para obtener los enlaces a los PDFs de un número de la revista
def obtener_enlaces_pdf(url_numero):
    try:
        response = requests.get(url_numero, timeout=(5, 30))  # Establecer un tiempo de espera para la conexión y la respuesta
        soup = BeautifulSoup(response.text, 'html.parser')
        enlaces_pdf = []
        base_url = 'http://www.economia.unam.mx'
        for enlace in soup.find_all('a', href=True):
            if enlace['href'].endswith('.pdf') and "publicareneconinfo.pdf" not in enlace['href'] and "PDI.pdf" not in enlace['href']:
                enlaces_pdf.append({
                    'url': base_url + enlace['href'],
                    'titulo': enlace.text.strip()  # Utilizar el texto del enlace como título del artículo
                })
        return enlaces_pdf
    except requests.exceptions.Timeout:
        print(f"Tiempo de espera agotado al intentar obtener los enlaces PDF desde {url_numero}")
        return []

# Limpiar el texto del título del artículo para que sea un nombre de archivo válido
def limpiar_nombre_archivo(texto):
    texto = re.sub(r'[\\/*?:"<>|]', '', texto)  # Eliminar caracteres no permitidos en nombres de archivo
    texto = re.sub(r'[^\x00-\x7F]+', '', texto)  # Eliminar caracteres no ASCII
    return texto[:100]  # Limitar la longitud del nombre del archivo a 100 caracteres

# Obtener la página índice
url_indice = 'http://www.economia.unam.mx/publicaciones/econinforma/wanteriores/anteriorl.html'
try:
    response_indice = requests.get(url_indice, timeout=(5, 30))  # Establecer un tiempo de espera para la conexión y la respuesta
    soup_indice = BeautifulSoup(response_indice.text, 'html.parser')
except requests.exceptions.Timeout:
    print(f"Tiempo de espera agotado al intentar obtener la página índice desde {url_indice}")

# Crear un directorio para guardar los PDFs descargados
if not os.path.exists('pdfs_econinfo'):
    os.makedirs('pdfs_econinfo')

# Recorrer los enlaces a los números de la revista en la página índice
for enlace_numero in soup_indice.find_all('a', href=True):
    if enlace_numero['href'].startswith('/assets/pdfs/econinfo/'):
        numero = enlace_numero.text.strip()
        url_numero = f"http://www.economia.unam.mx{enlace_numero['href']}"
        print(f"Descargando número {numero}...")

        # Obtener los enlaces a los PDFs de este número
        enlaces_pdf = obtener_enlaces_pdf(url_numero)

        # Crear un directorio para guardar los PDFs de este número
        nombre_directorio = f"pdfs_econinfo/{numero}"
        if not os.path.exists(nombre_directorio):
            os.makedirs(nombre_directorio)

        # Descargar cada PDF del número
        merger = PdfMerger()  # Inicializar el merger para el número actual
        for idx, enlace_pdf in enumerate(enlaces_pdf):
            titulo = limpiar_nombre_archivo(enlace_pdf['titulo'])
            nombre_archivo = f"{nombre_directorio}/{numero}_{idx + 1}_{titulo}.pdf"
            descargar_pdf(enlace_pdf['url'], nombre_archivo)
            print(f"Descargando {titulo}...")
            # Verificar que el archivo PDF se descargó correctamente antes de agregarlo al merger
            if os.path.isfile(nombre_archivo):
                merger.append(nombre_archivo)

        # Guardar el PDF combinado para este número
        nombre_pdf_combinado = f"pdfs_econinfo/{numero}.pdf"
        with open(nombre_pdf_combinado, 'wb') as f:
            merger.write(f)
        merger.close()
        print(f"PDF combinado para el número {numero} guardado correctamente.")

print("Todos los números de la revista han sido descargados y combinados.")