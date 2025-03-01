# import requests
# from bs4 import BeautifulSoup
# import os
# import time
# from urllib.parse import urljoin
# import re
# import urllib3

# # Deshabilitar advertencias de SSL (solo para pruebas)
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# class ElTrimestreEconomicoScraper:
#     def __init__(self):
#         self.base_url = "https://www.eltrimestreeconomico.com.mx"
#         self.archive_urls = [
#             f"{self.base_url}/index.php/te/issue/archive",
#             f"{self.base_url}/index.php/te/issue/archive/2",
#             f"{self.base_url}/index.php/te/issue/archive/3"
#         ]
#         self.output_dir = "pdf_eltrimestreeconomico"
#         self.headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
    
#     def create_directory(self, path):
#         if not os.path.exists(path):
#             os.makedirs(path)
    
#     def clean_filename(self, filename):
#         # Eliminar caracteres no válidos para nombres de archivo
#         return re.sub(r'[<>:"/\\|?*]', '', filename)
    
#     def get_issues(self):
#         issues = []
#         for archive_url in self.archive_urls:
#             response = requests.get(archive_url, headers=self.headers, verify=False)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 # Buscar cada bloque de issue
#                 for issue_block in soup.select('.issue-summary'):
#                     # Se toma el enlace de la página del número y el texto del volumen/número
#                     title_link = issue_block.select_one('.media-heading a')
#                     series_info = issue_block.select_one('.series.lead')
                    
#                     if title_link and series_info:
#                         issues.append({
#                             'title': series_info.text.strip(),  # Ejemplo: "Vol. 92 Núm. 365 (2025)"
#                             'url': urljoin(self.base_url, title_link['href'])
#                         })
#             time.sleep(1)
#         return issues
    
#     def get_articles_from_issue(self, issue_url):
#         articles = []
#         response = requests.get(issue_url, headers=self.headers, verify=False)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#             for article in soup.select('.article-summary.media'):
#                 title_elem = article.select_one('.media-heading a')
#                 # Se extrae el link del botón PDF
#                 pdf_link = article.select_one('.galley-link.btn.btn-primary.pdf')
                
#                 if title_elem and pdf_link:
#                     title = title_elem.text.strip()
#                     # La URL extraída es la del visor (view)
#                     pdf_url = urljoin(self.base_url, pdf_link['href'])
#                     articles.append({
#                         'title': title,
#                         'pdf_url': pdf_url
#                     })
#                 time.sleep(1)
#         return articles

#     def get_direct_download_url(self, view_url):
#         """
#         A partir de la URL para visualizar, se obtiene (o construye) la URL de descarga.
#         Se consulta la página del artículo y se busca, si es posible, el enlace de 'download'.
#         En muchos casos basta con reemplazar '/view/' por '/download/'.
#         """
#         # Primero, intentamos obtener la página del artículo
#         try:
#             response = requests.get(view_url, headers=self.headers, verify=False)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 # Se busca algún enlace que contenga '/download/' en su href
#                 download_link = soup.find('a', href=lambda h: h and '/download/' in h)
#                 if download_link and 'href' in download_link.attrs:
#                     return urljoin(self.base_url, download_link['href'])
#         except Exception as e:
#             print(f"Error al obtener la URL de descarga desde {view_url}: {str(e)}")
#         # Si no se encontró, se construye reemplazando '/view/' por '/download/'.
#         return view_url.replace('/view/', '/download/')
    
#     def download_pdf(self, view_url, filepath):
#         try:
#             # Obtener la URL directa de descarga
#             download_url = self.get_direct_download_url(view_url)
#             # Realiza la solicitud GET sin verificación SSL (como en la solución propuesta)
#             response = requests.get(download_url, verify=False)
#             if response.status_code == 200:
#                 # Grabar el contenido directamente en el archivo PDF
#                 with open(filepath, "wb") as f:
#                     f.write(response.content)
#                 return True
#             else:
#                 print(f"Error al descargar el PDF: Código de estado {response.status_code}")
#                 return False
#         except Exception as e:
#             print(f"Error al descargar {view_url}: {str(e)}")
#             return False

#     def run(self):
#         self.create_directory(self.output_dir)
#         issues = self.get_issues()
        
#         for issue in issues:
#             print(f"Procesando número: {issue['title']}")
#             # Crear carpeta usando el nombre del volumen/número
#             issue_dir = os.path.join(self.output_dir, self.clean_filename(issue['title']))
#             self.create_directory(issue_dir)
            
#             # Obtener los artículos de este número
#             articles = self.get_articles_from_issue(issue['url'])
#             for article in articles:
#                 filename = f"{self.clean_filename(article['title'])}.pdf"
#                 filepath = os.path.join(issue_dir, filename)
                
#                 print(f"Descargando: {article['title']}")
#                 if self.download_pdf(article['pdf_url'], filepath):
#                     print(f"Descargado exitosamente: {filename}")
#                 else:
#                     print(f"Error al descargar: {filename}")
                
#                 time.sleep(1)

# if __name__ == "__main__":
#     scraper = ElTrimestreEconomicoScraper()
#     scraper.run()




# implementacion deepseek

import requests
from bs4 import BeautifulSoup
import os
import time
import random
from urllib.parse import urljoin
import re
import urllib3
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ElTrimestreEconomicoScraper:
    def __init__(self):
        self.base_url = "https://www.eltrimestreeconomico.com.mx"
        self.archive_urls = [
            f"{self.base_url}/index.php/te/issue/archive",
            f"{self.base_url}/index.php/te/issue/archive/2",
            f"{self.base_url}/index.php/te/issue/archive/3"
        ]
        self.output_dir = "pdf_eltrimestreeconomico"
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_directory(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def clean_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '', filename)[:200]
    
    def get_issues(self):
        issues = []
        for archive_url in self.archive_urls:
            try:
                response = self.session.get(archive_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    for issue_block in soup.select('.issue-summary'):
                        title_link = issue_block.select_one('.media-heading a')
                        series_info = issue_block.select_one('.series.lead')
                        if title_link and series_info:
                            issues.append({
                                'title': series_info.text.strip(),
                                'url': urljoin(self.base_url, title_link['href'])
                            })
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                self.logger.error(f"Error obteniendo issues: {str(e)}")
        return issues
    
    def get_articles_from_issue(self, issue_url):
        articles = []
        try:
            response = self.session.get(issue_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for article in soup.select('.article-summary.media'):
                    title_elem = article.select_one('.media-heading a')
                    pdf_link = article.select_one('.galley-link.btn.btn-primary.pdf')
                    if title_elem and pdf_link:
                        articles.append({
                            'title': title_elem.text.strip(),
                            'pdf_url': urljoin(self.base_url, pdf_link['href'])
                        })
                    time.sleep(random.uniform(0.5, 2))
        except Exception as e:
            self.logger.error(f"Error obteniendo artículos: {str(e)}")
        return articles

    def get_direct_download_url(self, view_url):
        try:
            response = self.session.get(view_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                download_link = soup.find('a', class_='download')
                if download_link and download_link.get('href'):
                    return urljoin(self.base_url, download_link['href'])
            return None
        except Exception as e:
            self.logger.error(f"Error obteniendo URL directa: {str(e)}")
            return None
    
    def download_pdf(self, view_url, filepath):
        try:
            if os.path.exists(filepath):
                self.logger.info(f"Archivo ya existe: {os.path.basename(filepath)}")
                return True
                
            download_url = self.get_direct_download_url(view_url)
            if not download_url:
                self.logger.warning("URL de descarga no encontrada")
                return False
                
            response = self.session.get(download_url)
            
            if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
                with open(filepath, "wb") as f:
                    f.write(response.content)
                return True
            else:
                self.logger.error(f"Error HTTP {response.status_code} o contenido no PDF")
                return False
        except Exception as e:
            self.logger.error(f"Error descargando PDF: {str(e)}")
            return False

    def run(self):
        self.create_directory(self.output_dir)
        issues = self.get_issues()
        
        for issue in issues:
            self.logger.info(f"Procesando: {issue['title']}")
            issue_dir = os.path.join(self.output_dir, self.clean_filename(issue['title']))
            self.create_directory(issue_dir)
            
            articles = self.get_articles_from_issue(issue['url'])
            for article in articles:
                filename = f"{self.clean_filename(article['title'])}.pdf"
                filepath = os.path.join(issue_dir, filename)
                
                # Verificar si el archivo ya existe
                if os.path.exists(filepath):
                    self.logger.info(f"Saltando archivo existente: {filename}")
                    continue
                
                self.logger.info(f"Descargando: {article['title']}")
                if self.download_pdf(article['pdf_url'], filepath):
                    self.logger.info(f"Éxito: {filename}")
                else:
                    self.logger.error(f"Fallo: {filename}")
                
                time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    scraper = ElTrimestreEconomicoScraper()
    scraper.run()