import requests
import feedparser
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime

class ANSASportImageIntegrator:
    def __init__(self):
        self.rss_url = "https://www.ansa.it/sito/notizie/sport/sport_rss.xml"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_rss_feed(self):
        """Scarica e analizza il feed RSS di ANSA Sport"""
        try:
            response = self.session.get(self.rss_url, timeout=10)
            response.raise_for_status()
            return feedparser.parse(response.content)
        except Exception as e:
            print(f"Errore nel recupero del feed RSS: {e}")
            return None
    
    def extract_images_from_article(self, article_url):
        """Estrae le immagini da un singolo articolo"""
        try:
            response = self.session.get(article_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            images = []
            
            # Cerca immagini nell'articolo
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src')
                if src:
                    # Converti URL relativi in assoluti
                    full_url = urljoin(article_url, src)
                    # Filtra solo immagini di contenuto (non loghi, icone, ecc.)
                    if self.is_content_image(full_url, img):
                        images.append({
                            'url': full_url,
                            'alt': img.get('alt', ''),
                            'title': img.get('title', '')
                        })
            
            return images
        except Exception as e:
            print(f"Errore nell'estrazione immagini da {article_url}: {e}")
            return []
    
    def is_content_image(self, url, img_tag):
        """Determina se un'immagine è contenuto dell'articolo"""
        # Filtra loghi, icone e immagini di navigazione
        exclude_patterns = [
            'logo', 'icon', 'banner', 'ads', 'social',
            'navigation', 'header', 'footer', 'menu'
        ]
        
        url_lower = url.lower()
        alt_lower = img_tag.get('alt', '').lower()
        class_attr = ' '.join(img_tag.get('class', [])).lower()
        
        # Escludi se contiene pattern da escludere
        for pattern in exclude_patterns:
            if pattern in url_lower or pattern in alt_lower or pattern in class_attr:
                return False
        
        # Includi solo immagini di dimensioni ragionevoli
        width = img_tag.get('width')
        height = img_tag.get('height')
        if width and height:
            try:
                w, h = int(width), int(height)
                if w < 100 or h < 100:  # Troppo piccole
                    return False
            except ValueError:
                pass
        
        return True
    
    def create_wordpress_xml(self, feed_data):
        """Crea il file XML ottimizzato per WordPress"""
        # Crea root con namespace WordPress
        root = ET.Element('rss', {
            'version': '2.0',
            'xmlns:content': 'http://purl.org/rss/1.0/modules/content/',
            'xmlns:media': 'http://search.yahoo.com/mrss/',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:atom': 'http://www.w3.org/2005/Atom'
        })
        
        channel = ET.SubElement(root, 'channel')
        
        # Metadati del canale ottimizzati per WordPress
        ET.SubElement(channel, 'title').text = 'ANSA Sport - Feed WordPress'
        ET.SubElement(channel, 'link').text = feed_data.feed.get('link', 'https://www.ansa.it/sport/')
        ET.SubElement(channel, 'description').text = 'Feed RSS di ANSA Sport ottimizzato per WordPress con immagini integrate'
        ET.SubElement(channel, 'language').text = 'it-IT'
        ET.SubElement(channel, 'lastBuildDate').text = time.strftime('%a, %d %b %Y %H:%M:%S %z')
        ET.SubElement(channel, 'generator').text = 'ANSA Sport WordPress Integrator'
        
        # Link atom per self-reference
        atom_link = ET.SubElement(channel, '{http://www.w3.org/2005/Atom}link', {
            'href': 'https://your-domain.com/ansa-sport-feed.xml',
            'rel': 'self',
            'type': 'application/rss+xml'
        })
        
        # Processa ogni articolo
        for entry in feed_data.entries[:20]:  # Aumentato a 20 articoli
            print(f"Processando: {entry.title}")
            
            item = ET.SubElement(channel, 'item')
            
            # Dati base dell'articolo
            ET.SubElement(item, 'title').text = entry.title
            ET.SubElement(item, 'link').text = entry.link
            ET.SubElement(item, 'pubDate').text = entry.get('published', '')
            ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = entry.get('id', entry.link)
            
            # Categoria per WordPress
            ET.SubElement(item, 'category').text = 'Sport'
            
            # Autore (se disponibile)
            if hasattr(entry, 'author'):
                ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = entry.author
            else:
                ET.SubElement(item, '{http://purl.org/dc/elements/1.1/}creator').text = 'ANSA Sport'
            
            # Descrizione base
            description = entry.get('description', '')
            ET.SubElement(item, 'description').text = description
            
            # Estrai immagini dall'articolo
            images = self.extract_images_from_article(entry.link)
            
            # Crea contenuto arricchito con immagini per WordPress
            content_html = self.create_wordpress_content(description, images)
            
            # Contenuto completo per WordPress
            content_element = ET.SubElement(item, '{http://purl.org/rss/1.0/modules/content/}encoded')
            content_element.text = content_html
            
            # Media namespace per la prima immagine (featured image)
            if images:
                main_image = images[0]
                media_content = ET.SubElement(item, '{http://search.yahoo.com/mrss/}content', {
                    'url': main_image['url'],
                    'type': 'image/jpeg',
                    'medium': 'image'
                })
                
                if main_image['title']:
                    ET.SubElement(media_content, '{http://search.yahoo.com/mrss/}title').text = main_image['title']
                if main_image['alt']:
                    ET.SubElement(media_content, '{http://search.yahoo.com/mrss/}description').text = main_image['alt']
            
            # Pausa per evitare sovraccarico del server
            time.sleep(1)
        
        return root
    
    def create_wordpress_content(self, description, images):
        """Crea contenuto HTML ottimizzato per WordPress"""
        content_parts = []
        
        # Aggiungi la descrizione originale
        if description:
            content_parts.append(f'<p>{description}</p>')
        
        # Aggiungi le immagini come HTML
        if images:
            content_parts.append('<div class="ansa-images">')
            for i, img in enumerate(images[:3]):  # Massimo 3 immagini
                img_html = f'''
                <figure class="wp-block-image size-large">
                    <img src="{img['url']}" alt="{img['alt']}" title="{img['title']}" />
                    {f'<figcaption>{img["title"]}</figcaption>' if img['title'] else ''}
                </figure>
                '''
                content_parts.append(img_html)
            content_parts.append('</div>')
        
        return '\n'.join(content_parts)
    
    def save_xml(self, root, filename='wordpress_ansa_sport_feed.xml'):
        """Salva il file XML formattato per WordPress"""
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent='  ', encoding='utf-8')
        
        with open(filename, 'wb') as f:
            f.write(pretty_xml)
        
        print(f"File XML WordPress salvato come: {filename}")
    
    def run(self):
        """Esegue il processo completo per WordPress"""
        print("Avvio creazione feed WordPress per ANSA Sport...")
        
        # Scarica il feed RSS
        feed_data = self.fetch_rss_feed()
        if not feed_data:
            print("Impossibile recuperare il feed RSS")
            return
        
        print(f"Feed RSS caricato: {len(feed_data.entries)} articoli trovati")
        
        # Crea XML ottimizzato per WordPress
        wordpress_xml = self.create_wordpress_xml(feed_data)
        
        # Salva il file
        self.save_xml(wordpress_xml)
        
        print("Feed WordPress creato con successo!")
        print("\nPer utilizzare il feed in WordPress:")
        print("1. Carica il file XML sul tuo server")
        print("2. Usa un plugin come 'WP RSS Aggregator' o 'FeedWordPress'")
        print("3. Configura l'URL del feed nel plugin")
        print("4. Le immagini saranno automaticamente integrate nei post")

if __name__ == "__main__":
    integrator = ANSASportImageIntegrator()
    integrator.run()
