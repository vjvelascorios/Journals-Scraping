!pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin

# Lista de URLs a scrapear
urls = [
    "http://herzog.economia.unam.mx/academia/inae/index.php/inae-i",
    "http://herzog.economia.unam.mx/academia/inae/index.php/inae-ii",
    "http://herzog.economia.unam.mx/academia/inae/index.php/inae-iii",
    "http://herzog.economia.unam.mx/academia/inae/index.php/inae-iv",
    "http://herzog.economia.unam.mx/academia/inae/index.php/inae-v"
]

# Función para descargar los PDFs de una URL dada
def descargar_pdfs(url):
    # Realizamos la solicitud GET a la página
    response = requests.get(url)
    
    # Verificamos si la solicitud fue exitosa
    if response.status_code == 200:
        # Parseamos el contenido HTML
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Encontramos todos los enlaces que contienen la palabra "pdf"
        pdf_links = soup.find_all("a", href=lambda href: (href and href.endswith(".pdf")))
        
        # Extraemos el texto relevante del enlace para determinar la carpeta de destino
        folder_match = re.search(r'/inae-(\w+)', url)
        if folder_match:
            carpeta = folder_match.group(1)
        else:
            carpeta = "pdfs"
        
        # Creamos el directorio para almacenar los archivos PDF si no existe
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        
        # Descargamos cada PDF y lo guardamos con su nombre correcto
        for link in pdf_links:
            pdf_url = link["href"]
            # Comprobamos si la URL del PDF tiene un esquema especificado
            if not pdf_url.startswith("http"):
                pdf_url = urljoin(url, pdf_url)
            pdf_nombre = link.text.strip()
            # Eliminamos caracteres no permitidos en los nombres de archivos y truncamos el nombre si es necesario
            pdf_nombre = "".join(x for x in pdf_nombre if x.isalnum() or x in [" ", ".", "_"])[:100].rstrip()
            pdf_ruta = os.path.join(carpeta, f"{pdf_nombre}.pdf")
            # Descargamos el PDF
            with open(pdf_ruta, "wb") as pdf_file:
                pdf_response = requests.get(pdf_url)
                pdf_file.write(pdf_response.content)
            print(f"Descargado: {pdf_ruta}")
    else:
        print(f"No se pudo obtener la página: {url}")

# Procesamos cada URL en la lista
for url in urls:
    descargar_pdfs(url)


!mkdir inae
!mv i*/ inae
!mv v*/ inae
!tar -cvf inae.tar inae/