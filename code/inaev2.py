# inae v2

import asyncio
import logging
from pathlib import Path
from typing import List, Optional
import aiohttp
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf_downloader.log'),
        logging.StreamHandler()
    ]
)

class PDFDownloader:
    def __init__(self, urls: List[str], output_dir: str = "pdfs_inae", rate_limit: float = 1.0):
        self.urls = urls
        self.output_dir = Path(output_dir)
        self.rate_limit = rate_limit
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()

    async def download_pdf(self, url: str, filename: str) -> bool:
        """
        Download a single PDF file asynchronously if it doesn't exist.
        
        Args:
            url: URL of the PDF file
            filename: Output filename
        
        Returns:
            bool: True if file exists or download successful, False otherwise
        """
        file_path = self.output_dir / filename
        
        # Verificar si el archivo ya existe
        if file_path.exists():
            logging.info(f"Archivo {filename} ya existe, omitiendo descarga")
            return True
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        logging.info(f"Descargado exitosamente: {filename}")
                        return True
                    else:
                        logging.error(f"Error al descargar {url}: Status {response.status}")
                        return False
        except Exception as e:
            logging.error(f"Error al descargar {url}: {str(e)}")
            return False

    def get_pdf_links(self, url: str) -> List[str]:
        """
        Extract PDF links from a webpage.
        
        Args:
            url: Webpage URL
        
        Returns:
            List of PDF URLs
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, "html.parser")
            pdf_links = soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))
            
            return [urljoin(url, link['href']) for link in pdf_links]
        except Exception as e:
            logging.error(f"Error parsing {url}: {str(e)}")
            return []

    async def process_url(self, url: str) -> None:
        """Process a single URL and download its PDFs."""
        pdf_links = self.get_pdf_links(url)
        if not pdf_links:
            logging.warning(f"No PDF links found in {url}")
            return

        for link in tqdm(pdf_links, desc=f"Processing {url}"):
            filename = Path(link).name
            await self.download_pdf(link, filename)
            await asyncio.sleep(self.rate_limit)  # Rate limiting

    async def download_all(self) -> None:
        """Download PDFs from all URLs concurrently."""
        tasks = [self.process_url(url) for url in self.urls]
        await asyncio.gather(*tasks)

def main():
    urls = [
        "http://herzog.economia.unam.mx/academia/inae/index.php/inae-i",
        "http://herzog.economia.unam.mx/academia/inae/index.php/inae-ii",
        "http://herzog.economia.unam.mx/academia/inae/index.php/inae-iii",
        "http://herzog.economia.unam.mx/academia/inae/index.php/inae-iv",
        "http://herzog.economia.unam.mx/academia/inae/index.php/inae-v"
    ]

    downloader = PDFDownloader(urls)
    asyncio.run(downloader.download_all())

if __name__ == "__main__":
    main()